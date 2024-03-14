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
    w_id: int
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
    

class DynamicSchema(BaseModel):
    id: int
    w_id: int
    dynamic_id: int
    dynamic_pub_ts: int
    dynamic_pub_time: str
    
    class Config:
        from_attributes = True
        
class FullDynamicDataSchema(BaseModel):
    id: int
    author: str
    uid: str
    platform: str
    core: str
    add_time: int
    watch_type: str
    
    
    dynamic_id: int
    dynamic_pub_ts: int
    dynamic_pub_time: str
    download_status: DownloadStatus
    download_path: str
    