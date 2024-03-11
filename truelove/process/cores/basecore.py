from abc import ABC, abstractmethod

class BaseCore(ABC):
    def __init__(self):
        pass
    
    @abstractmethod
    async def download_video(self, md):
        pass