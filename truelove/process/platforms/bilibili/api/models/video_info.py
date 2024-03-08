from typing import List
from pydantic import BaseModel


class VideoInfoDescV2(BaseModel):
    raw_text: str
    type: int
    biz_id: int
    
class VideoInfoRights(BaseModel):
    bp: int
    elec: int
    download: int
    movie: int
    pay: int
    hd5: int
    no_reprint: int
    autoplay: int
    ugc_pay: int
    is_cooperation: int
    ugc_pay_preview: int
    no_background: int
    clean_mode: int
    is_stein_gate: int
    is_360: int
    no_share: int
    arc_pay: int
    free_watch: int


class VideoInfoPagesDimension(BaseModel):
    width: int
    height: int
    rotate: int
   

class VideoInfoOwner(BaseModel):
    mid: int
    name: str
    face: str
    
class VideoInfoStat(BaseModel):
    aid: int
    view: int
    danmaku: int
    reply: int
    favorite: int
    coin: int
    share: int
    now_rank: int
    his_rank: int
    like: int
    dislike: int
    evaluation: str
    vt: int
    
class VideoInfoPages(BaseModel):
    cid: int
    page: int
    # from: str
    part: str
    duration: int
    vid: str
    weblink: str
    # dimension: VideoInfoPagesDimension

class VideoInfo(BaseModel):
    bvid: str
    aid: int
    videos: int
    tid: int
    tname: str
    copyright: int
    pic: str
    title: str
    pubdate: int
    ctime: int
    desc: str
    desc_v2: List[VideoInfoDescV2]
    state: int
    # attribute: int
    duration: int
    # forward: int
    # mission_id: int
    # redirect_url: str
    # rights:  VideoInfoRights
    owner:  VideoInfoOwner
    stat:   VideoInfoStat
    dynamic: str
    cid: int
    dimension:  VideoInfoPagesDimension
    # premiere: Optional[None]
    # teenage_mode: int
    # is_chargeable_season: bool
    # is_story: bool
    # no_cache: bool
    pages: List[VideoInfoPages]
    # subtitle: Dict[str, Any]
    # staff: List[Dict[str, Any]]
    # is_season_display: bool
    # user_garb: Dict[str, Any]
    # honor_reply: Dict[str, Any]
    # like_icon: str
    # argue_info: Dict[str, Any]

