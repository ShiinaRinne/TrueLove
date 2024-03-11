from abc import ABC, abstractmethod
from truelove.db.models.schema import WatcheeSchema, VideoSchema, FullVideoDataSchema

class BaseManager(ABC):
    @abstractmethod
    async def add_watchee_to_db(self, uid: str, platform: str, core: str, watch_type: str) -> WatcheeSchema:
        pass

    @abstractmethod
    async def save_watchee_videos_info_to_db(self, w: WatcheeSchema, *args, **kwargs):
        pass

    @abstractmethod
    async def download_dynamic(self, w: WatcheeSchema, *args, **kwargs):
        pass

    @abstractmethod
    async def download_video(self, f: FullVideoDataSchema):
        pass
