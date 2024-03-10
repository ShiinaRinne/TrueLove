import os
import asyncio

from typing import List, Optional
from apscheduler.schedulers.asyncio import AsyncIOScheduler

from truelove.config import config
from truelove.logger import logger
from truelove.process.utils import *
from truelove.process.exception import *
from truelove.process.event import tl_event_mgr
from truelove.db import VideoDB, WatchingDB
from truelove.db.models.schema import DownloadStatus
from truelove.db.models import WatcheeSchema, FullVideoDataSchema

from truelove.process.cores import core_managers
from truelove.process.platforms import platform_managers

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
    async def add_watchee(uid: str, platform: str, core: str, watch_type: str) -> WatcheeSchema | None:
        if (pmgr:= platform_managers.get(platform)) is None:
            raise PlatformNotFoundException(f"Platform {platform} not found")
        
        is_exists = await WatchingDB.is_watchee_exists_in_db(uid)
        if is_exists is not None:
            logger.warning(f"Author [{uid}] already exists")
            return None
    
        return await pmgr.add_watchee_to_db(uid=uid, platform=platform, core=core, watch_type=watch_type)

    @staticmethod
    async def remove_watchee(uid: str, delete_videos: bool = False) -> bool:
        watchee_info: List[WatcheeSchema] = await WatchingDB.fetch_watchee_info_from_db(uid)

        # cant find
        if watchee_info is None or len(watchee_info) == 0:
            return False

        await WatchingDB.delete_author(watchee_info[0])
        
        if delete_videos:
            video_download_paths:List[str] = await VideoDB.fetch_video_save_path(watchee_info[0])
            await TrueLoveManager.__delete_files(video_download_paths)
            await VideoDB.delete_author_video(watchee_info[0])
            
        return True
    
    @staticmethod
    async def refresh_watchee(uid: Optional[str] = None, *args, **kwargs) -> None:
        if task_in_progress.get("refresh", False):
            return {"message": "任务正在进行中, 请稍后再试"}
        
        task_in_progress["refresh"] = True
        try:
            watchees: List[WatcheeSchema] = await WatchingDB.fetch_watchee_info_from_db(uid=uid)
            sem = asyncio.Semaphore(4)
            tasks = [TrueLoveManager.__save_watchee_videos_to_db(a, *args, **kwargs) for a in watchees]
        
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
            os.remove(p)
            
            # just for test
            # dir_name = os.path.dirname(p)
            # base_name = os.path.basename(p)
            # new_name = f"_deleted_{base_name}"
            # new_path = os.path.join(dir_name, new_name)
            # os.rename(p, new_path)

    @staticmethod
    async def __save_watchee_videos_to_db(w: WatcheeSchema, *args, **kwargs):
        if (pmgr:= platform_managers.get(w.platform)) is None:
            raise PlatformNotFoundException(f"Platform {w.platform} not found")
        
        await pmgr.save_watchee_videos_to_db(w, *args, **kwargs)
    
    @staticmethod
    async def __download_video(t: FullVideoDataSchema):
        if (pmgr:= platform_managers.get(t.platform)) is None:
            raise PlatformNotFoundException(f"Platform {t.platform} not found")
        if (cmgr:= core_managers.get(t.core)) is None:
            raise CoreNotFoundException(f"Core {t.core} not found")

        t.download_path = parse_save_dir(t) # 未下载的文件的 download_path 是空的, 这里正好可以塞进去直接给后面用
        
        (t,), _ = await tl_event_mgr.emit("before_download", t)
        
        await cmgr.download_video(t)

        await VideoDB.update_video_download_status(t, DownloadStatus.SUCCESS)
        
        await tl_event_mgr.emit("after_download", t)

