from truelove.db.models.schema import WatcheeSchema, VideoSchema, FullVideoDataSchema

class BaseCore:
    def __init__(self):
        pass
    
    async def download_video(self, md):
        raise NotImplementedError