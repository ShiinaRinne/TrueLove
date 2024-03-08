import os
import asyncio
import subprocess

from datetime import datetime
from typing import List, Optional, Any, Union
from apscheduler.schedulers.asyncio import AsyncIOScheduler

from truelove.config import config
from truelove.logger import logger
from truelove.process.utils import *
from truelove.process.exception import *
from truelove.db import MediaDB, WatchingDB
from truelove.db.models import WatcheeSchema, MediaSchema, FullMediaDataSchema



task_in_progress = {}

AVAILABLE_PLATFORM = {
    "bilibili": ["bilix", 
                #  "you-get"
                 ],
    # "youtube": ["youtube-dl", "you-get"],
}


class TrueLoveManager:
    scheduler: AsyncIOScheduler = AsyncIOScheduler()
    cores = []

    def __init__(self):
        # self.core_dir = config.root_dir / "bin"
        pass

    @staticmethod
    def update_core():
        core_list = os.listdir(config.root_dir / "bin")
        for core in core_list:
            TrueLoveManager.cores.append(core)

        exist = subprocess.run(["bilix", "--version"], capture_output=True, text=True)
        if exist.returncode == 0:
            TrueLoveManager.cores.append("bilix")

    # TODO: use watchee instead of bili.AuthorInfo
    @staticmethod
    async def add_watchee(uid: str, platform: str, core: str) -> WatcheeSchema | None:
        is_exists = await WatchingDB.is_watchee_exists_in_db(uid)
        if is_exists is not None:
            logger.warning(f"Author [{uid}] already exists")
            return None

        match platform:
            case "bilibili":
                from truelove.process.platforms.bilibili import BiliBiliManager

                return await BiliBiliManager.add_watchee(uid=uid, platform=platform, core=core)
                
            case _:
                pass

    @staticmethod
    async def save_watchee_medias_to_db(w: WatcheeSchema):
        match w.platform:
            case "bilibili":
                from truelove.process.platforms.bilibili import BiliBiliManager

                await BiliBiliManager.save_watchee_medias_to_db(w)
            case _:
                pass

    @staticmethod
    async def fetch_watchee_info(uid: Optional[str] = None) -> List[WatcheeSchema]:
        return await WatchingDB.fetch_watchee_info_from_db(uid)

    @staticmethod
    async def refresh(uid: Optional[str] = None):
        logger.info("Refresh~~~")
        watchees: List[WatcheeSchema] = await WatchingDB.fetch_watchee_info_from_db(
            uid=uid
        )

        sem = asyncio.Semaphore(4)
        tasks = [TrueLoveManager.save_watchee_medias_to_db(a) for a in watchees]
        try:
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
    async def download(t: FullMediaDataSchema):
        if t.core not in TrueLoveManager.cores:
            raise CoreNotFoundException(f"Core {t.core} not found")
        match t.platform:
            case "bilibili":
                from truelove.process.platforms.bilibili import BiliBiliManager
                await BiliBiliManager.download(t)
            case _:
                pass
        
        await TrueLoveManager._download_cover(t)


    @staticmethod
    async def _download_cover(t:FullMediaDataSchema):
        cover = t.media_cover
        dir = parse_save_dir(t)
        
        # bilibili use bilix to download cover
        pass
        
        
        

    @staticmethod
    async def remove_watchee(uid: str, delete_medias: bool = False) -> bool:
        watchee_info: List[WatcheeSchema] = await WatchingDB.fetch_watchee_info_from_db(
            uid
        )

        # cant find
        if watchee_info is None or len(watchee_info) == 0:
            return False

        await WatchingDB.delete_author(uid)

        if delete_medias:
            medias: List[MediaSchema] = await MediaDB.fetch_media_by_author_from_db(
                watchee_info[0].w_id
            )
            for m in medias:
                await MediaDB.delete_media(m.media_id)
        return True

    @staticmethod
    def add_job(trigger: str, args: List[Any], minutes: int = 1, id: str = "default"):
        TrueLoveManager.scheduler.add_job(
            sync_wrapper,
            trigger,
            args=args,
            minutes=minutes,
            next_run_time=datetime.now(),
            id=id,
        )

    @staticmethod
    async def download_media():
        ws: List[FullMediaDataSchema] = (
            await TrueLoveManager.fetch_watchee_content_from_db(limit=1, status=0)
        )
        for w in ws:
            await TrueLoveManager.download(w)

        # TODO: After download event