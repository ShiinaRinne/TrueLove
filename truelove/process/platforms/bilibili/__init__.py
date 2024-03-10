import asyncio
from typing import AsyncGenerator, List

from ..base import BaseManager

from truelove.logger import logger
from truelove.process.exception import *
from truelove.db import VideoDB, WatchingDB
from truelove.db.models.schema import WatcheeSchema, VideoSchema, FullVideoDataSchema
from truelove.process.platforms.bilibili.api.models import AuthorVideoSearchVList
from truelove.process.cores import core_managers
from truelove.process.platforms.bilibili.api import *


class BiliBiliManager(BaseManager):
    
    @staticmethod
    async def add_watchee_to_db(uid: str, platform: str, core:str, watch_type: str) -> WatcheeSchema:
        author_info: AuthorInfo = await BiliBiliManager.__fetch_author_info(int(uid))
        await WatchingDB.add_author(name=author_info.name, uid=uid, platform=platform, core=core, watch_type=watch_type)
        
        return (await WatchingDB.fetch_watchee_info_from_db(uid=uid))[0]
    
    @staticmethod
    async def save_watchee_videos_to_db(w: WatcheeSchema, *args, **kwargs):
        current_video_id = await BiliBiliManager.__fetch_current_video_id_list_from_db(w)

        async for v in BiliBiliManager.__fetch_videos(w.uid):
            if str(v.bvid) in current_video_id:
                logger.info(f"Video [{v.title}] already exists, skip {w.author} [{w.uid}]")
                if kwargs.get("force_refresh", False): 
                    continue
                return
            
            video_info = await BiliAPI.fetch_video_info(v.bvid)
            await VideoDB.add_video_to_db(
                w_id=w.w_id,
                video_id=video_info.bvid,
                video_name=video_info.title,
                video_cover=video_info.pic,
                video_intro=video_info.desc,
                video_created=video_info.ctime,
                video_pubdate=video_info.pubdate,
                video_num=video_info.videos,
            )
            logger.info(f"Add [{v.title}] to Video. Wait for download~")


    @staticmethod
    async def __fetch_author_info(mid: int) -> AuthorInfo | None:
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
    async def __fetch_current_video_id_list_from_db(w: WatcheeSchema) -> List[str]:
        videos: List[VideoSchema] = await VideoDB.fetch_video_list_by_author_from_db(w.w_id)
        
        return [m.video_id for m in videos]
    
    
    @staticmethod
    async def __fetch_videos(uid: str) -> AsyncGenerator[AuthorVideoSearchVList, None]:
        page1 = await BiliAPI.fetch_author_video_list(uid, pn=1)
        count = page1.page.count
        if count > 0:
            for video in page1.list.vlist:
                yield video
        
        for pn in range(1, count // 30 + 1):
            videos_page = await BiliAPI.fetch_author_video_list(uid, pn=pn + 1)
            for video in videos_page.list.vlist:
                yield video

