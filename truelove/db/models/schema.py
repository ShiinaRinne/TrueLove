from pydantic import BaseModel

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
    download_status: int
    
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
    download_status: int
    
