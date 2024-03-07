import asyncio
from typing import AsyncGenerator, List

from .base import BaseManager
from truelove.db import MediaDB, WatchingDB
from truelove.db.models import WatcheeSchema, MediaSchema, FullMediaDataSchema
from truelove.process.exception import *
from truelove.process.platforms.api.biliapi import *
from truelove.process.utils import parse_save_dir
from truelove.logger import logger


async def read_output(process):
    while True:
        line = await process.stdout.readline()
        if not line:
            break
        print(line.decode().strip())


class BiliBiliManager(BaseManager):
    def __init__(self) -> None:
        pass
        

    @staticmethod
    async def fetch_author_info(mid: int) -> AuthorInfo | None:
        """查询用户基础信息

        Args:
            mid (int): 用户mid

        Returns:
            UpInfo: _description_
        """
        url = "https://api.bilibili.com/x/space/wbi/acc/info"
        result = await BiliAPI._request(url, params=get_params(mid))
        
        return AuthorInfo.model_validate(result["data"])
        
    @staticmethod
    async def add_watchee(uid: str, platform: str, core:str) -> AuthorInfo | None:
        author_info: AuthorInfo = await BiliBiliManager.fetch_author_info(int(uid))
        await WatchingDB.add_author(name=author_info.name, uid=uid, platform=platform, core=core)
        
        return author_info
    
    @staticmethod
    async def _fetch_current_medias_id_from_db(w: WatcheeSchema):
        medias: List[MediaSchema] = await MediaDB.fetch_media_by_author_from_db(w.w_id)
        medias_id = [m.media_id for m in medias]
        return medias_id
    
    @staticmethod
    async def _fetch_videos(uid: str) -> AsyncGenerator[AuthorVideoSearchVList, None]:
        page1 = await BiliAPI.fetch_author_video_list(uid, pn=1)
        count = page1.page.count
        if count > 0:
            for video in page1.list.vlist:
                yield video
        
        for pn in range(1, count // 30 + 1):
            videos_page = await BiliAPI.fetch_author_video_list(uid, pn=pn + 1)
            for video in videos_page.list.vlist:
                yield video
            await asyncio.sleep(30)

    @staticmethod
    async def save_watchee_medias_to_db(w: WatcheeSchema):
        current_medias_id = await BiliBiliManager._fetch_current_medias_id_from_db(w)

        async for v in BiliBiliManager._fetch_videos(w.uid):
            if str(v.bvid) in current_medias_id:
                logger.info(f"Media [{v.title}] already exists, skip {w.author} [{w.uid}]")
                return 
                continue 

            video_info = await BiliAPI.fetch_video_info(v.bvid)
            await MediaDB.add_media_to_db(
                w_id=w.w_id,
                media_id=video_info.bvid,
                media_type="video",
                media_name=video_info.title,
                media_cover=video_info.pic,
                media_intro=video_info.desc,
                media_created=video_info.ctime,
            )
            logger.info(f"Add [{v.title}] to Medias. Wait for download~")

            await asyncio.sleep(5)

    @staticmethod
    async def download(md: FullMediaDataSchema):
        match md.core :
            case "bilix":
                await BiliBiliManager.download_bilix(md)
            case _:
                raise CoreNotFoundException(f"Core {md.core} not supported on {md.platform}")

    @staticmethod
    async def download_bilix(md: FullMediaDataSchema) -> str:
        # cmd = BiliBiliManager.core_dir / "bilix"
        download_url = f"https://www.bilibili.com/video/{md.media_id}"
        cmd = "bilix" # install bilix with pip, no need to use absolute path
        if md.media_type == "video":
                params = [
                    str(cmd),
                    "get_series" if md.media_videos > 1 else "v",
                    download_url,
                    "-d",
                    parse_save_dir(md),
                    "--cookie",
                    config.cookie
                ]
        else:
            raise UnsupportedMediaTypeException(
                f"Media type {md.media_type} not supported on bilix"
            )
        logger.info(
            f"Download {md.platform} -> {md.author} -> {md.media_name} started"
        )
        process = await asyncio.create_subprocess_exec(*params, stdout=asyncio.subprocess.PIPE, stderr=asyncio.subprocess.PIPE)
        asyncio.create_task(read_output(process))

        returncode = await process.wait()
        if returncode != 0:
            stderr = await process.stderr.read()
            raise DownloadFailedException(md, stderr=stderr)
        
        await MediaDB.update_media_download_status(md.media_id, 1)

        return "Download completed."
