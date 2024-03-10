import os
import asyncio
import subprocess

from typing import List, Optional
from apscheduler.schedulers.asyncio import AsyncIOScheduler

from truelove.config import config
from truelove.logger import logger
from truelove.process.utils import *
from truelove.process.exception import *
from truelove.process.event import tl_event_mgr
from truelove.db import MediaDB, WatchingDB
from truelove.db.models.schema import DownloadStatus
from truelove.db.models import WatcheeSchema, FullMediaDataSchema



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


    cores = []
    @staticmethod
    def update_core():
        core_list = os.listdir(config.root_dir / "bin")
        for core in core_list:
            TrueLoveManager.cores.append(core)

        exist = subprocess.run(["bilix", "--version"], capture_output=True, text=True)
        if exist.returncode == 0:
            TrueLoveManager.cores.append("bilix")


    @staticmethod
    async def add_watchee(uid: str, platform: str, core: str) -> WatcheeSchema | None:
        is_exists = await WatchingDB.is_watchee_exists_in_db(uid)
        if is_exists is not None:
            logger.warning(f"Author [{uid}] already exists")
            return None

        match platform:
            case "bilibili":
                from truelove.process.platforms.bilibili import BiliBiliManager
                return await BiliBiliManager.add_watchee_to_db(uid=uid, platform=platform, core=core)
                
            case _:
                pass


    @staticmethod
    async def save_watchee_medias_to_db(w: WatcheeSchema, *args, **kwargs):
        match w.platform:
            case "bilibili":
                from truelove.process.platforms.bilibili import BiliBiliManager
                await BiliBiliManager.save_watchee_medias_to_db(w, *args, **kwargs)
            case _:
                pass


    @staticmethod
    async def fetch_watchee_info(uid: Optional[str] = None) -> List[WatcheeSchema]:
        return await WatchingDB.fetch_watchee_info_from_db(uid)


    @staticmethod
    async def refresh(uid: Optional[str] = None, *args, **kwargs):
        if task_in_progress.get("refresh", False):
            return {"message": "任务正在进行中, 请稍后再试"}
        
        task_in_progress["refresh"] = True
        try:
            watchees: List[WatcheeSchema] = await WatchingDB.fetch_watchee_info_from_db(uid=uid)
            sem = asyncio.Semaphore(4)
            tasks = [TrueLoveManager.save_watchee_medias_to_db(a, *args, **kwargs) for a in watchees]
        
            await asyncio.gather(*(sem_coro(sem, t) for t in tasks))
        finally:
            task_in_progress["refresh"] = False


    @staticmethod
    async def fetch_watchee_content_from_db(
        limit: int = 99,
        order_by: str = "add_time",
        order: Literal["asc", "desc"] = "desc",
        uid: Optional[str] = None,
        status: Optional[int] = None,
    ) -> List[FullMediaDataSchema]:
        return await WatchingDB.fetch_watchee_content_from_db(
            limit=limit, order_by=order_by, order=order, uid=uid, status=status
        )


    @staticmethod
    async def _download(t: FullMediaDataSchema):
        if t.core not in TrueLoveManager.cores:
            raise CoreNotFoundException(f"Core {t.core} not found")
        t.download_path = parse_save_dir(t) # 未下载的文件的 download_path 是空的, 这里正好可以塞进去直接给后面用
        
        (t,), _ = await tl_event_mgr.emit("before_download", t)
        
        await TrueLoveManager._download_video(t)
        await TrueLoveManager._download_cover(t)
        
        await MediaDB.update_media_download_status(t, DownloadStatus.SUCCESS)
        
        await tl_event_mgr.emit("after_download", t)


    @staticmethod
    async def _download_video(t:FullMediaDataSchema):
        match t.platform:
            case "bilibili":
                from truelove.process.platforms.bilibili import BiliBiliManager
                await BiliBiliManager._download(t)
            case _:
                pass


    @staticmethod
    async def _download_cover(t:FullMediaDataSchema):
        cover = t.media_cover
        dir = t.download_path
        
        # bilibili use bilix to download cover
        pass


    @staticmethod
    async def _delete_files(paths: List[str]):
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
    async def remove_watchee(uid: str, delete_medias: bool = False) -> bool:
        watchee_info: List[WatcheeSchema] = await WatchingDB.fetch_watchee_info_from_db(uid)

        # cant find
        if watchee_info is None or len(watchee_info) == 0:
            return False

        await WatchingDB.delete_author(watchee_info[0])
        
        if delete_medias:
            media_download_paths:List[str] = await MediaDB.fetch_media_save_path(watchee_info[0])
            await TrueLoveManager._delete_files(media_download_paths)
            await MediaDB.delete_author_media(watchee_info[0])
            
        return True


    @staticmethod
    async def download_media():
        ws: List[FullMediaDataSchema] = (
            await TrueLoveManager.fetch_watchee_content_from_db(limit=1, status=0, order_by="media_pubdate", order="asc")
        )
        for w in ws:
            await TrueLoveManager._download(w)