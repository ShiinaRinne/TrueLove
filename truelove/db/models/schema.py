from enum import Enum
from pydantic import BaseModel

class DownloadStatus(Enum):
    NOT_DOWNLOADED  = 0
    SUCCESS         = 1
    
class VideoSchema(BaseModel):
    id: int
    w_id: int
    video_id: str
    video_name: str
    video_cover: str
    video_intro: str
    video_created: str
    video_pubdate: int
    video_num: int
    download_status: DownloadStatus
    download_path: str
    
    class Config:
        from_attributes = True
        
class WatcheeSchema(BaseModel):
    w_id: int
    author: str
    uid: str
    platform: str
    core: str
    add_time: int
    watch_type: str

    class Config:
        from_attributes = True

class FullVideoDataSchema(BaseModel):
    id: int
    author: str
    uid: str
    platform: str
    core: str
    add_time: int
    watch_type: str
    
    video_id: str
    video_name: str
    video_cover: str
    video_intro: str
    video_created: str
    video_pubdate: int
    video_num: int
    download_status: DownloadStatus
    download_path: str
    
