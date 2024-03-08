from enum import Enum
from pydantic import BaseModel

class DownloadStatus(Enum):
    NOT_DOWNLOADED  = 0
    SUCCESS         = 1
    
class MediaSchema(BaseModel):
    id: int
    w_id: int
    media_id: str
    media_type: str
    media_name: str
    media_cover: str
    media_intro: str
    media_created: str
    media_pubdate: int
    media_videos: int
    download_status: DownloadStatus
    
    class Config:
        from_attributes = True
        
class WatcheeSchema(BaseModel):
    w_id: int
    author: str
    uid: str
    platform: str
    core: str
    add_time: int

    class Config:
        from_attributes = True

class FullMediaDataSchema(BaseModel):
    id: int
    author: str
    uid: str
    platform: str
    core: str
    add_time: int
    
    media_id: str
    media_type: str
    media_name: str
    media_cover: str
    media_intro: str
    media_created: str
    media_pubdate: int
    media_videos: int
    download_status: DownloadStatus
    
