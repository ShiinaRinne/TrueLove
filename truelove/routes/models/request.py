from pydantic import BaseModel
from typing import Optional, Union, Literal


class AddWatcheeRequest(BaseModel):
    uid: str
    platform: Optional[str] = "bilibili"
    core: Literal["bilix", "you-get"] = "bilix"
    watch_type: Literal["video", "dynamic"]

class RemoveSubscriptionRequest(BaseModel):
    w_id:  int
    watch_type: Literal["video", "dynamic"]
    delete_downloads: bool = False
