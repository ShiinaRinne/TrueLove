from typing import List, Literal
from sqlalchemy import asc, desc
from sqlalchemy.orm import Session
from sqlalchemy.sql import select, delete, update
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from truelove.db.models import Media, MediaSchema
from truelove.db import session_handler
from truelove.logger import logger

class MediaDB:
    @staticmethod
    @session_handler
    async def add_media_to_db(
        w_id: int,
        media_id: str,
        media_type: str,
        media_name: str,
        media_cover: str,
        media_intro: str,
        media_created: int, # b站视频投稿时间
        media_pubdate: int = 0, # b站视频发布时间
        media_videos: int = 1, # b站分p总数, 默认为1
        download_status: int = 0,
        session: Session = None,
    ) -> None:
        media = Media(
            w_id=w_id,
            media_id=media_id,
            media_type=media_type,
            media_name=media_name,
            media_cover=media_cover,
            media_intro=media_intro,
            media_created=media_created,
            media_pubdate=media_pubdate,
            media_videos=media_videos,
            download_status=download_status,
        )
        try:
            session.add(media)
        except IntegrityError:
            pass


    @staticmethod
    @session_handler
    async def update_media_download_status(
        media_id: str,
        download_status: int,
        session: Session = None,
    ) -> None:
        await session.execute(update(Media).where(Media.media_id == media_id).values(download_status=download_status))

    
    @staticmethod
    @session_handler
    async def fetch_media_by_author_from_db(
        w_id: int,
        limit: int = 999,
        order_by: str = "media_created",
        order: Literal["asc", "desc"] = "desc",
        session: AsyncSession = None,
    ) -> List[MediaSchema]:
        """指定作者的id, 获取作者当前全部media

        Args:
            session (Session): _description_
            w_id (int): _description_
            limit (int, optional): _description_. Defaults to 10.
            order_by (str, optional): _description_. Defaults to "created".
            order (Literal[&quot;asc&quot;, &quot;desc&quot;], optional): _description_. Defaults to "asc".

        Returns:
            List[Media]: _description_
        """
        order_function = asc if order == "asc" else desc
        order_expression = order_function(getattr(Media, order_by))
        return (
            (
                await session.execute(
                    select(Media)
                    .filter(Media.w_id == w_id)
                    .order_by(order_expression)
                    .limit(limit)
                )
            )
            .scalars()
            .all()
        )

    @staticmethod
    @session_handler
    async def delete_media(media_id: str, session: Session = None) -> None:
        logger.info(f"Delete [{media_id}] from Medias")
        await session.execute(delete(Media).filter(Media.media_id == media_id))
