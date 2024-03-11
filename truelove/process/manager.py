import shutil
import asyncio

from typing import List, Optional
from apscheduler.schedulers.asyncio import AsyncIOScheduler

from truelove.config import config
from truelove.logger import logger
from truelove.process.utils import *
from truelove.process.exception import *
from truelove.process.event import tl_event_mgr

from truelove.process.platforms import platform_managers

from truelove.db import VideoDB, WatchingDB, DynamicDB
from truelove.db.models.schema import DownloadStatus
from truelove.db.models import WatcheeSchema, FullVideoDataSchema


task_in_progress = {}

AVAILABLE_PLATFORM = {
    "bilibili": ["bilix", 
                #  "you-get"
                 ],
    # "youtube": ["youtube-dl", "you-get"],
}


class TrueLoveManager:
    scheduler: AsyncIOScheduler = AsyncIOScheduler()

    @staticmethod
    async def trigger_job_manually(job_id: str, *args, **kwargs):
        job = next((job for job in TrueLoveManager.scheduler.get_jobs() if job.id == job_id), None)
        if job: await job.func(*args, **kwargs) # job.modify(next_run_time=datetime.now())


    @staticmethod
    async def add_watchee(uid: str, platform: str, core: str, watch_type: str) -> bool:
        if (pmgr:= platform_managers.get(platform)) is None:
            raise PlatformNotFoundException(f"Platform {platform} not found")
        
        is_exists = await WatchingDB.is_watchee_exists_in_db(uid, watch_type)
        if is_exists is not None:
            logger.warning(f"Author [{uid}] already exists")
            return False
    
        await pmgr.add_watchee_to_db(uid=uid, platform=platform, core=core, watch_type=watch_type)
        return True

    @staticmethod
    async def remove_watchee(w_id: int, watch_type:Literal["video", "dynamic"], delete_downloads: bool = False) -> bool:
        watchee_info: List[WatcheeSchema] = await WatchingDB.fetch_watchee_info_from_db(w_id, watch_type=watch_type)

        # cant find
        if watchee_info is None or len(watchee_info) == 0:
            return False

        await WatchingDB.delete_author(watchee_info[0])
        
        if delete_downloads:
            match watch_type:
                case "video":
                    media_download_paths:List[str] = await VideoDB.fetch_video_save_path(watchee_info[0])
                    await VideoDB.delete_author_video(watchee_info[0])
                case "dynamic":
                    media_download_paths:List[str] = await DynamicDB.fetch_dynamic_save_path(watchee_info[0])
                    await DynamicDB.delete_author_dynamic(watchee_info[0])
                    
            await TrueLoveManager.__delete_files(media_download_paths)
            
        return True
    
    @staticmethod
    async def refresh_watchee(w_id: Optional[int] = None, *args, **kwargs) -> None:
        if task_in_progress.get("refresh", False):
            return {"message": "任务正在进行中, 请稍后再试"}
        
        task_in_progress["refresh"] = True
        try:
            watchees: List[WatcheeSchema] = await WatchingDB.fetch_watchee_info_from_db(w_id=w_id)
            sem = asyncio.Semaphore(4)
            tasks = [TrueLoveManager.__refresh_watchee(w, *args, **kwargs) for w in watchees]
        
            await asyncio.gather(*(sem_coro(sem, t) for t in tasks))
        finally:
            task_in_progress["refresh"] = False
 
    @staticmethod
    async def fetch_watchee_info(uid: Optional[str] = None) -> List[WatcheeSchema]:
        return await WatchingDB.fetch_watchee_info_from_db(uid)

    @staticmethod
    async def fetch_watchee_video_list(
            limit: int = 99,
            order_by: str = "add_time",
            order: Literal["asc", "desc"] = "desc",
            uid: Optional[str] = None,
            status: Optional[int] = None,
        ) -> List[FullVideoDataSchema]:
        return await WatchingDB.fetch_watchee_video_list_from_db(
                    limit=limit, order_by=order_by, order=order, uid=uid, status=status
                )

    @staticmethod
    async def download_video():
        ws: List[FullVideoDataSchema] = (await TrueLoveManager.fetch_watchee_video_list(limit=1, status=0, order_by="video_pubdate", order="asc"))
        for w in ws:
            await TrueLoveManager.__download_video(w)


    @staticmethod
    async def __delete_files(paths: List[str]):
        for p in paths:
            if not os.path.exists(p):
                continue
            try:
                shutil.rmtree(p)
            except PermissionError as e:
                logger.error(f"Can't remove {p}. \r\nPermissionError: {repr(e)}")
            
            # just for test
            # dir_name = os.path.dirname(p)
            # base_name = os.path.basename(p)
            # new_name = f"_deleted_{base_name}"
            # new_path = os.path.join(dir_name, new_name)
            # os.rename(p, new_path)

    @staticmethod
    async def __refresh_watchee(w: WatcheeSchema, *args, **kwargs):
        if (pmgr:= platform_managers.get(w.platform)) is None:
            raise PlatformNotFoundException(f"Platform {w.platform} not found")
        
        match w.watch_type:
            case "video":
                await pmgr.save_watchee_videos_info_to_db(w, *args, **kwargs)
            case "dynamic":
                await pmgr.download_dynamic(w, *args, **kwargs)
            case _:
                logger.warning(f"Unknown watch_type {w.watch_type}")
                return
    
    @staticmethod
    async def __download_video(t: FullVideoDataSchema):
        if (pmgr:= platform_managers.get(t.platform)) is None:
            raise PlatformNotFoundException(f"Platform {t.platform} not found")
        

        t.download_path = parse_save_dir(t.author, t.video_name, t.platform, t.watch_type) # 未下载的文件的 download_path 是空的, 这里正好可以塞进去直接给后面用
        
        (t,), _ = await tl_event_mgr.emit("before_download", t)
        
        await pmgr.download_video(t)

        await VideoDB.update_video_download_status(t, DownloadStatus.SUCCESS)
        
        await tl_event_mgr.emit("after_download", t)

