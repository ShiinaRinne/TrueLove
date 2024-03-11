import aiofiles
from aiohttp import ClientSession
from typing import AsyncGenerator, List

from truelove.logger import logger
from truelove.process.exception import *
from truelove.process.cores import core_managers
from truelove.process.platforms.base import BaseManager
from truelove.db import VideoDB, WatchingDB, DynamicDB
from truelove.db.models.schema import WatcheeSchema, VideoSchema, FullVideoDataSchema, FullDynamicDataSchema, DownloadStatus
from truelove.process.platforms.bilibili.api.models import AuthorVideoSearchVList
from truelove.process.platforms.bilibili.api import *
from truelove.process.platforms.bilibili.api.models.dynamic_info import DynamicDataItems, DynamicDataItemsType, DynamicDataItemsMajorType
class BiliBiliManager(BaseManager):
    async def add_watchee_to_db(self, uid: str, platform: str, core:str, watch_type: str) -> None:
        author_info: AuthorInfo = await self.__fetch_author_info(int(uid))
        await WatchingDB.add_author(name=author_info.name, uid=uid, platform=platform, core=core, watch_type=watch_type)

    
    
    async def save_watchee_videos_info_to_db(self, w: WatcheeSchema, *args, **kwargs):
        current_video_id_list:List[str] = await self.__fetch_current_video_id_list_from_db(w)

        async for v in self.__fetch_videos(w.uid):
            if str(v.bvid) in current_video_id_list:
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


    async def download_video(self, v: FullVideoDataSchema) -> None:
        if (cmgr:= core_managers.get(v.core)) is None:
            raise CoreNotFoundException(f"Core {v.core} not found")
        await cmgr.download_video(v)


    async def download_dynamic(self, w: WatcheeSchema, *args, **kwargs):
        async for dynamic in self.__fetch_dynamics(w.uid):
            is_dynamic_exists = await DynamicDB.is_dynamic_exists_in_db(w.w_id, dynamic.id_str)
            if is_dynamic_exists: continue
            m = dynamic.modules.module_dynamic.major
            a = dynamic.modules.module_author
            
            match dynamic.type:
                case DynamicDataItemsType.DYNAMIC_TYPE_DRAW:
                    match m.type:
                        case DynamicDataItemsMajorType.MAJOR_TYPE_OPUS:
                            o = m.opus
                            save_dir = await self.save_dynamic(w, name = f"{a.pub_ts}", content = o.summary.text, pic_urls = [pic.url for pic in o.pics])
                            await DynamicDB.add_dynamic_to_db(w.w_id, dynamic.id_str, a.pub_ts, a.pub_time, DownloadStatus.SUCCESS, save_dir)
                        case _:
                            await self.save_unsupported_dynamic(w, dynamic, a)

                case DynamicDataItemsType.DYNAMIC_TYPE_WORD:
                    m = dynamic.modules.module_dynamic.major
                    match m.type:
                        case DynamicDataItemsMajorType.MAJOR_TYPE_OPUS:
                            o = m.opus
                            save_dir = await self.save_dynamic(w, name = f"{a.pub_ts}", content = o.summary.text)
                            await DynamicDB.add_dynamic_to_db(w.w_id, dynamic.id_str, a.pub_ts, a.pub_time, DownloadStatus.SUCCESS, save_dir)

                        case _:
                            await self.save_unsupported_dynamic(w, dynamic, a)
                case _:
                    await self.save_unsupported_dynamic(w, dynamic, a)

    async def save_unsupported_dynamic(self, w: WatcheeSchema, dynamic: DynamicDataItems, a,) -> None:
        logger.error(f"暂不支持的动态类型: {dynamic.type}. \r\n{dynamic}")
        save_dir = await self.save_dynamic(w, name = f"{a.pub_ts}", content = dynamic.model_dump_json(), file_ext="json")
        await DynamicDB.add_dynamic_to_db(w.w_id, dynamic.id_str, a.pub_ts, a.pub_time, DownloadStatus.SUCCESS, save_dir)
    
    
    async def save_dynamic(self, w: WatcheeSchema, name: str, content: str, pic_urls: List[str] = [], file_ext: str = "txt") -> str:
        from truelove.process.utils import parse_save_dir
        save_dir = parse_save_dir(w.author, name, w.platform, w.watch_type)
        async with aiofiles.open(f"{save_dir}/{name}.{file_ext}", "w", encoding="utf-8") as f:
            await f.write(content)

        async with ClientSession() as session:
            for pic_url in pic_urls:
                async with session.get(pic_url) as response:
                    if response.status == 200:
                        pic_content = await response.read()
                        pic_name = pic_url.split("/")[-1]
                        async with aiofiles.open(f"{save_dir}/{pic_name}", "wb") as f:
                            await f.write(pic_content)
                
        logger.info(f"Save dynamic {name}.{file_ext} to {save_dir}")
        
        return save_dir

    async def __fetch_author_info(self, mid: int) -> AuthorInfo | None:
        """查询用户基础信息

        Args:
            mid (int): 用户mid

        Returns:
            UpInfo: _description_
        """
        url = "https://api.bilibili.com/x/space/wbi/acc/info"
        result = await BiliAPI._request(url, params=get_params(mid))
        
        return AuthorInfo.model_validate(result["data"])
    
    
    async def __fetch_current_video_id_list_from_db(self, w: WatcheeSchema) -> List[str]:
        videos: List[VideoSchema] = await VideoDB.fetch_video_list_by_author_from_db(w.w_id)
        
        return [m.video_id for m in videos]
    
    
    async def __fetch_videos(self, uid: str) -> AsyncGenerator[AuthorVideoSearchVList, None]:
        page1 = await BiliAPI.fetch_author_video_list(uid, pn=1)
        count = page1.page.count
        if count > 0:
            for video in page1.list.vlist:
                yield video
        
        for pn in range(1, count // 30 + 1):
            videos_page = await BiliAPI.fetch_author_video_list(uid, pn=pn + 1)
            for video in videos_page.list.vlist:
                yield video
    
    
    async def __fetch_dynamics(self, uid: str):
        has_more = True
        offset = ''
        while has_more:
            dynamic_data = await BiliAPI.fetch_author_dynamics(uid, offset=offset)
            has_more = dynamic_data.has_more
            offset = dynamic_data.offset
            
            items:List[DynamicDataItems] = dynamic_data.items
            for item in items:
                yield item
                
            if not has_more:
                break
                
