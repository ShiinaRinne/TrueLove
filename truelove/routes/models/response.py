from typing import Optional
from pydantic import BaseModel

class SubscriptionResponse(BaseModel):
    id: int
    author: str
    uid: str
    platform: str
    add_time: int
    
    video_id: str
    video_name: str
    video_cover: str
    video_intro: str
    video_created: str
    download_status: int
    
    
class AddWatcheeResponse(BaseModel):
    status: str
    message: Optional[str] = None
    uid: Optional[int] = None
    platform: Optional[str] = None
    watch_type: Optional[str] = None
    ret_code: int

