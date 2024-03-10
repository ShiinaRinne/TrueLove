from typing import AsyncGenerator
from truelove.db.models.schema import WatcheeSchema, VideoSchema, FullVideoDataSchema

class BaseManager:
    
    @staticmethod
    async def add_watchee_to_db(uid: str, platform: str, core:str, watch_type: str) -> WatcheeSchema:
        raise NotImplementedError
       
    @staticmethod
    async def save_watchee_videos_to_db(w: WatcheeSchema, *args, **kwargs):
         raise NotImplementedError

