from pydantic import BaseModel
from typing import Optional, Union, Literal


class AddWatcheeRequest(BaseModel):
    uid: str
    platform: Optional[str] = "bilibili"
    core: Literal["bilix", "you-get"] = "bilix"

class RemoveSubscriptionRequest(BaseModel):
    uid: Union[str, int]
    delete_medias: bool = False
