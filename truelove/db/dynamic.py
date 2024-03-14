from typing import List
from sqlalchemy.orm import Session
from sqlalchemy.sql import select, delete
from sqlalchemy.exc import IntegrityError

from truelove.db import session_handler
from truelove.db.models import Dynamic
from truelove.db.models.schema import DownloadStatus, FullVideoDataSchema, VideoSchema, WatcheeSchema

class DynamicDB:
    @staticmethod
    @session_handler
    async def add_dynamic_to_db(w_id: int, dynamic_id: str,dynamic_pub_ts:int = -1, dynamic_pub_time: str = "", download_status:DownloadStatus = DownloadStatus.NOT_DOWNLOADED, download_path: str = "", session: Session = None) -> None:
        dynamic = Dynamic(
            w_id=w_id,
            dynamic_id=dynamic_id,
            dynamic_pub_ts=dynamic_pub_ts,
            dynamic_pub_time=dynamic_pub_time,
            download_status=download_status.value,
            download_path=download_path,
        )
        try:
            session.add(dynamic)
        except IntegrityError:
            pass
        
        
    @staticmethod
    @session_handler
    async def is_dynamic_exists_in_db(w_id: int, dynamic_id: str, session: Session = None) -> bool:
        return (await session.execute(select(Dynamic).where(Dynamic.w_id == w_id, Dynamic.dynamic_id == dynamic_id))).scalar() is not None
    
    @staticmethod
    @session_handler
    async def fetch_dynamic_save_path(w: WatcheeSchema, session: Session = None) -> List[str]:
        data = (await session.execute(select(Dynamic.download_path).filter(Dynamic.w_id == w.w_id))).scalars().all()
        return data
    
    @staticmethod
    @session_handler
    async def delete_author_dynamic(w: WatcheeSchema, session: Session = None) -> None:
        await session.execute(delete(Dynamic).where(Dynamic.w_id == w.w_id))

    