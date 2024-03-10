from typing import List, Literal
from sqlalchemy import asc, desc
from sqlalchemy.orm import Session
from sqlalchemy.sql import select, delete, update
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from truelove.logger import logger
from truelove.db import session_handler
from truelove.db.models import Video
from truelove.db.models.schema import DownloadStatus, FullVideoDataSchema, VideoSchema, WatcheeSchema

class VideoDB:
    @staticmethod
    @session_handler
    async def add_video_to_db(
        w_id: int,
        video_id: str,
        video_name: str,
        video_cover: str,
        video_intro: str,
        video_created: int,
        video_pubdate: int,
        video_num: int,
        download_status: int = 0,
        session: Session = None,
    ) -> None:
        video = Video(
            w_id=w_id,
            video_id=video_id,
            video_name=video_name,
            video_cover=video_cover,
            video_intro=video_intro,
            video_created=video_created,
            video_pubdate=video_pubdate,
            video_num=video_num,
            download_status=download_status,
        )
        try:
            session.add(video)
        except IntegrityError:
            pass


    @staticmethod
    @session_handler
    async def update_video_download_status(
        t:FullVideoDataSchema,
        download_status: DownloadStatus,
        session: Session = None,
    ) -> None:
        """更新文件的下载状态与下载路径

        Args:
            t (FullVideoDataSchema): _description_
            download_status (DownloadStatus): _description_
            session (Session, optional): _description_. Defaults to None.
        """
        await session.execute(update(Video).where(Video.video_id == t.video_id).values(download_status=download_status.value, download_path=t.download_path))

    @staticmethod
    @session_handler
    async def update_video_download_path(video_id: str, download_path: str, session: Session = None) -> None:
        await session.execute(update(Video).where(Video.video_id == video_id).values(download_path=download_path))

    
    @staticmethod
    @session_handler
    async def fetch_video_list_by_author_from_db(
        w_id: int,
        limit: int = 999,
        order_by: str = "video_created",
        order: Literal["asc", "desc"] = "desc",
        session: AsyncSession = None,
    ) -> List[VideoSchema]:
        """指定作者的id, 获取作者当前全部video

        Args:
            session (Session): _description_
            w_id (int): _description_
            limit (int, optional): _description_. Defaults to 10.
            order_by (str, optional): _description_. Defaults to "created".
            order (Literal[&quot;asc&quot;, &quot;desc&quot;], optional): _description_. Defaults to "asc".

        Returns:
            List[Video]: _description_
        """
        order_function = asc if order == "asc" else desc
        order_expression = order_function(getattr(Video, order_by))
        return (
            (
                await session.execute(
                    select(Video)
                    .filter(Video.w_id == w_id)
                    .order_by(order_expression)
                    .limit(limit)
                )
            )
            .scalars()
            .all()
        )


    @staticmethod
    @session_handler
    async def delete_author_video(w: WatcheeSchema, session: Session = None) -> None:
        logger.info(f"Delete [{w.platform} - {w.author}] from Video")
        await session.execute(delete(Video).filter(Video.w_id == w.w_id))

    
    @staticmethod
    @session_handler
    async def fetch_video_save_path(w: WatcheeSchema, session: Session = None) -> List[str]:
        return (await session.execute(select(Video.download_path).filter(Video.w_id == w.w_id))).scalars().all()
        
