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
    FullMediaDataSchema,
    Media,
    MediaSchema,
)
from truelove.logger import logger


class WatchingDB:
    @staticmethod
    @session_handler
    async def fetch_watchee_content_from_db(
        limit: int = 99,
        order_by: str = "media_pubdate",
        order: Literal["asc", "desc"] = "desc",
        uid: Optional[str] = None,
        status: Optional[int] = None,
        session: AsyncSession = None,
    ) -> List[FullMediaDataSchema]:
        order_function = asc if order == "asc" else desc
        order_expression = order_function(getattr(Media, order_by))

        class _Response(BaseModel):
            Media: MediaSchema
            Watching: WatcheeSchema

        q = select(Media, Watching).join(Watching, Media.w_id == Watching.w_id)
        
        if uid is not None: q = q.filter(Watching.uid == uid)
        if status is not None: q = q.filter(Media.download_status == status)
            
        result: List[_Response] = (await session.execute(q.order_by(order_expression).limit(limit))).mappings().all()  
        
        return [
            FullMediaDataSchema(
                id=r.Media.w_id,
                author=r.Watching.author,
                uid=r.Watching.uid,
                platform=r.Watching.platform,
                core = r.Watching.core,
                add_time=r.Watching.add_time,
                media_id=r.Media.media_id,
                media_type=r.Media.media_type,
                media_name=r.Media.media_name,
                media_cover=r.Media.media_cover,
                media_intro=r.Media.media_intro,
                media_created=r.Media.media_created,
                media_pubdate=r.Media.media_pubdate,
                media_videos=r.Media.media_videos,
                download_status=r.Media.download_status,
                download_path=r.Media.download_path,
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
        add_time: int = int(time.time()),
        session: AsyncSession = None,
    ) -> None:
        logger.info(f"Add [{uid} - {name}]  to Watching")
        w = Watching(author=name, uid=str(uid), platform=platform,core=core, add_time=add_time)
        session.add(w)
        
        

    @staticmethod
    @session_handler
    async def delete_author(
        w: WatcheeSchema,
        session: AsyncSession = None,
    ) -> None:
        logger.info(f"Delete [{w.platform} - {w.author}] from Watching")
        await session.execute(delete(Watching).filter(Watching.uid == str(w.uid)))
        

    @staticmethod
    @session_handler
    async def is_watchee_exists_in_db(uid: str, session: AsyncSession = None) -> WatcheeSchema | None:
        return (await session.execute(select(Watching).filter(Watching.uid == uid))).scalars().first()
        

    @staticmethod
    @session_handler
    async def fetch_watchee_info_from_db(
        uid:Optional[str] = None,
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
        if uid is not None:
            query = query.filter(Watching.uid == uid)
        result = await session.execute(query.limit(limit))
        return result.scalars().all()
