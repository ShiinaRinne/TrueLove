from typing import AsyncGenerator


class BaseManager:
    def __init__(self, *args, **kwargs):
        pass
    
    async def _fetch_videos(self, uid: str) -> AsyncGenerator:
        pass
    
    async def __check_core(self):
        pass
    
    async def save_watchee_medias_to_db(self):
        pass
    
    async def download(self):
        pass
    
    @staticmethod
    async def add_watchee(uid: str, platform: str, core:str):
        pass
    
    async def after_download(self):
        pass