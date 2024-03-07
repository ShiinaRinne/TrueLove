from typing import Optional
from pydantic import BaseModel

class SubscriptionResponse(BaseModel):
    id: int
    author: str
    uid: str
    platform: str
    add_time: int
    
    media_id: str
    media_name: str
    media_cover: str
    media_intro: str
    media_created: str
    download_status: int
    
    
class AddWatcheeResponse(BaseModel):
    status: str
    message: Optional[str] = None
    uid: Optional[int] = None
    platform: Optional[str] = None
    ret_code: int

