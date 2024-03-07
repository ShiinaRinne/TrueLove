from typing import Optional, Union, Literal
from pydantic import BaseModel

class AddWatcheeRequest(BaseModel):
    uid: str
    platform: Optional[str] = "bilibili"
    core: Literal["bilix", "you-get"] = "bilix"

class RemoveSubscriptionRequest(BaseModel):
    uid: Union[str, int]
    delete_medias: bool = False
