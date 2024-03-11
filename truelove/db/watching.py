import time
from pydantic import BaseModel
from typing import List, Literal, Optional, Union
from sqlalchemy import asc, desc
from sqlalchemy.sql import select, delete
from sqlalchemy.ext.asyncio import AsyncSession

from truelove.db import session_handler
from truelove.db.models import (
    Watching,
    WatcheeSchema,
    FullVideoDataSchema,
    Video,
    VideoSchema,
)
from truelove.logger import logger


class WatchingDB:
    @staticmethod
    @session_handler
    async def fetch_watchee_video_list_from_db(
        limit: int = 99,
        order_by: str = "video_pubdate",
        order: Literal["asc", "desc"] = "desc",
        uid: Optional[str] = None,
        status: Optional[int] = None,
        session: AsyncSession = None,
    ) -> List[FullVideoDataSchema]:
        order_function = asc if order == "asc" else desc
        order_expression = order_function(getattr(Video, order_by))

        class _Response(BaseModel):
            Video: VideoSchema
            Watching: WatcheeSchema

        q = select(Video, Watching).join(Watching, Video.w_id == Watching.w_id)
        
        if uid is not None: q = q.filter(Watching.uid == uid)
        if status is not None: q = q.filter(Video.download_status == status)
            
        result: List[_Response] = (await session.execute(q.order_by(order_expression).limit(limit))).mappings().all()  
        
        return [
            FullVideoDataSchema(
                id=r.Video.w_id,
                author=r.Watching.author,
                uid=r.Watching.uid,
                platform=r.Watching.platform,
                core = r.Watching.core,
                add_time=r.Watching.add_time,
                watch_type=r.Watching.watch_type,
                video_id=r.Video.video_id,
                video_name=r.Video.video_name,
                video_cover=r.Video.video_cover,
                video_intro=r.Video.video_intro,
                video_created=r.Video.video_created,
                video_pubdate=r.Video.video_pubdate,
                video_num=r.Video.video_num,
                download_status=r.Video.download_status,
                download_path=r.Video.download_path,
            )
            for r in result
        ]

    @staticmethod
    @session_handler
    async def add_author(
        name: str,
        uid: str,
        platform: str,
        core: str,
        watch_type:str,
        add_time: int = int(time.time()),
        session: AsyncSession = None,
    ) -> None:
        logger.info(f"Add [{uid} - {name}]  to Watching")
        w = Watching(author=name, uid=str(uid), platform=platform,core=core, add_time=add_time, watch_type=watch_type)
        session.add(w)
        
        

    @staticmethod
    @session_handler
    async def delete_author(
        w: WatcheeSchema,
        session: AsyncSession = None,
    ) -> None:
        logger.info(f"Delete [{w.platform} - {w.author}] from Watching")
        await session.execute(delete(Watching).filter(Watching.w_id == w.w_id))
        

    @staticmethod
    @session_handler
    async def is_watchee_exists_in_db(uid: str, watch_type: str, session: AsyncSession = None) -> WatcheeSchema | None:
        return (await session.execute(select(Watching).filter(Watching.uid == uid, Watching.watch_type==watch_type))).scalars().first()
        

    @staticmethod
    @session_handler
    async def fetch_watchee_info_from_db(
        w_id:Optional[int] = None,
        watch_type:Optional[str] = None,
        limit: int = 999,
        order_by: str = "add_time",
        order: Literal["asc", "desc"] = "desc",
        session: AsyncSession = None,
    ) -> List[WatcheeSchema]:
        """获取全部关注的作者信息

        Args:
            session (Session): _description_
            limit (int, optional): _description_. Defaults to 10.
            order_by (str, optional): _description_. Defaults to "add_time".
            order (Literal[&quot;asc&quot;, &quot;desc&quot;], optional): _description_. Defaults to "asc".

        Returns:
            List[Watching]: _description_
        """
        order_function = asc if order == "asc" else desc
        order_expression = order_function(getattr(Watching, order_by))
        query = select(Watching).order_by(order_expression)
        if w_id is not None:
            query = query.filter(Watching.w_id == w_id)
        if watch_type is not None:
            query = query.filter(Watching.watch_type == watch_type)
        result = await session.execute(query.limit(limit))
        return result.scalars().all()
