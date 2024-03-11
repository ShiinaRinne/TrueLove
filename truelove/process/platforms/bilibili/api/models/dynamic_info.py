from enum import Enum
from pydantic import BaseModel, Field
from typing import Any, List, Optional, Union


class DynamicDataItemsBasicCommentType(Enum):
    UNKNOWN = 0
    DYNAMIC_TYPE_AV = 1
    DYNAMIC_TYPE_PGC = 1
    DYNAMIC_TYPE_UGC_SEASON = 1
    DYNAMIC_TYPE_DRAW = 11
    DYNAMIC_TYPE_ARTICLE = 12
    DYNAMIC_TYPE_LIVE_RCMD = 17
    DYNAMIC_TYPE_FORWARD = 17
    DYNAMIC_TYPE_WORD = 17
    DYNAMIC_TYPE_COMMON_SQUARE = 17
    DYNAMIC_TYPE_LIVE = 17
    DYNAMIC_TYPE_MEDIALIST = 19


class DynamicDataItemsBasicCommentIdStr(Enum):
    DYNAMIC_TYPE_AV = "视频AV号"
    DYNAMIC_TYPE_PGC = "剧集分集AV号"
    DYNAMIC_TYPE_UGC_SEASON = "视频AV号"
    DYNAMIC_TYPE_DRAW = "相簿id"
    DYNAMIC_TYPE_ARTICLE = "专栏cv号"
    DYNAMIC_TYPE_LIVE_RCMD = "动态本身id"
    DYNAMIC_TYPE_FORWARD = "动态本身id"
    DYNAMIC_TYPE_WORD = "动态本身id"
    DYNAMIC_TYPE_COMMON_SQUARE = "动态本身id"
    DYNAMIC_TYPE_LIVE = "动态本身id"
    DYNAMIC_TYPE_MEDIALIST = "收藏夹ml号"


class DynamicDataItemsBasic(BaseModel):
    comment_id_str: str
    comment_type: DynamicDataItemsBasicCommentType
    rid_str: str


class DynamicDataItemsMajorType(Enum):
    MAJOR_TYPE_NONE = "MAJOR_TYPE_NONE"  # 动态失效 716510857084796964
    MAJOR_TYPE_FORWARD = "MAJOR_TYPE_FORWARD" # 动态转发 866756840240709701
    MAJOR_TYPE_OPUS = "MAJOR_TYPE_OPUS" # 图文动态 870176712256651305
    MAJOR_TYPE_ARCHIVE = "MAJOR_TYPE_ARCHIVE" # 视频 716526237365829703
    MAJOR_TYPE_PGC = "MAJOR_TYPE_PGC" # 剧集更新 645981661420322824
    MAJOR_TYPE_COURSES = "MAJOR_TYPE_COURSES" #
    MAJOR_TYPE_DRAW = "MAJOR_TYPE_DRAW" # 带图动态 716358050743582725
    MAJOR_TYPE_ARTICLE = "MAJOR_TYPE_ARTICLE" #
    MAJOR_TYPE_MUSIC = "MAJOR_TYPE_MUSIC" # 音频更新
    MAJOR_TYPE_COMMON = "MAJOR_TYPE_COMMON" # 一般类型 716481612656672789
    MAJOR_TYPE_LIVE = "MAJOR_TYPE_LIVE" # 直播间分享 267505569812738175
    MAJOR_TYPE_MEDIALIST = "MAJOR_TYPE_MEDIALIST" #
    MAJOR_TYPE_APPLET = "MAJOR_TYPE_APPLET" #
    MAJOR_TYPE_SUBSCRIPTION = "MAJOR_TYPE_SUBSCRIPTION" #
    MAJOR_TYPE_LIVE_RCMD = "MAJOR_TYPE_LIVE_RCMD" # 直播状态
    MAJOR_TYPE_UGC_SEASON = "MAJOR_TYPE_UGC_SEASON" # 合计更新 716509100448415814
    MAJOR_TYPE_SUBSCRIPTION_NEW = "MAJOR_TYPE_SUBSCRIPTION_NEW" #
    
    
    

class DynamicDataItemsType(Enum):
    DYNAMIC_TYPE_NONE = "DYNAMIC_TYPE_NONE"  # 716510857084796964 无效动态
    DYNAMIC_TYPE_FORWARD = "DYNAMIC_TYPE_FORWARD" # 动态转发
    DYNAMIC_TYPE_AV = "DYNAMIC_TYPE_AV" # 投稿视频
    DYNAMIC_TYPE_PGC = "DYNAMIC_TYPE_PGC" # 
    # DYNAMIC_TYPE_COURSES = ?
    DYNAMIC_TYPE_WORD = "DYNAMIC_TYPE_WORD"  # 718377531474968613 # 纯文字动态
    DYNAMIC_TYPE_DRAW = "DYNAMIC_TYPE_DRAW"  # 718384798557536290 # 带图动态

    DYNAMIC_TYPE_ARTICLE = "DYNAMIC_TYPE_ARTICLE"  # 718372214316990512 # 投稿专栏
    DYNAMIC_TYPE_MUSIC = "DYNAMIC_TYPE_MUSIC" # "音乐"
    DYNAMIC_TYPE_COMMON_SQUARE = "DYNAMIC_TYPE_COMMON_SQUARE"  # 551309621391003098, 716503778995470375, 716481612656672789 # 装扮, 剧集点评, 普通分享
    DYNAMIC_TYPE_LIVE = "DYNAMIC_TYPE_LIVE"  # 718371505648435205
    DYNAMIC_TYPE_MEDIALIST = "DYNAMIC_TYPE_MEDIALIST"  # 534428265320147158 # 收藏夹
    DYNAMIC_TYPE_COURSES_SEASON = "DYNAMIC_TYPE_COURSES_SEASON"  # 717906712866062340 # 课程
    # DYNAMIC_TYPE_COURSES_BATCH = ?
    # DYNAMIC_TYPE_AD = ?
    # DYNAMIC_TYPE_APPLET = ?
    # DYNAMIC_TYPE_SUBSCRIPTION = ?
    DYNAMIC_TYPE_LIVE_RCMD = "DYNAMIC_TYPE_LIVE_RCMD"  # 718371505648435205 直播开播
    # DYNAMIC_TYPE_BANNER = ?
    DYNAMIC_TYPE_UGC_SEASON = "DYNAMIC_TYPE_UGC_SEASON"  # 718390979031203873 合集更新
    DYNAMIC_TYPE_PGC_UNION = "DYNAMIC_TYPE_PGC_UNION" # ?
    # DYNAMIC_TYPE_SUBSCRIPTION_NEW = ?


class DynamicDataItemsModulesModuleAuthorType(Enum):
    AUTHOR_TYPE_NONE = "AUTHOR_TYPE_NONE" # 无效动态
    AUTHOR_TYPE_NORMAL = "AUTHOR_TYPE_NORMAL" # 普通更新
    AUTHOR_TYPE_PGC = "AUTHOR_TYPE_PGC" # 剧集更新
    AUTHOR_TYPE_UGC_SEASON = "AUTHOR_TYPE_UGC_SEASON" # 合集更新


class DynamicDataItemsModulesModuleAuthor(BaseModel):
    face: str
    following: Union[bool, None]
    jump_url: str
    label: str
    mid: int
    name: str
    pub_action: str
    # pub_location_text: str
    pub_time: str
    pub_ts: int
    type: DynamicDataItemsModulesModuleAuthorType


class DynamicDataItemsModulesModuleDynamicDescRichTextNodes(BaseModel):
    orig_text: str
    text: str
    type: str
    emoji: Optional[Any] = Field(default=None)
    jump_url: Optional[str] = Field(default=None)
    rid: Optional[str] = Field(default=None)
    # goods: Optional[Any] = Field(default=None)
    # icon_name: str


class DynamicDataItemsModulesModuleDynamicDesc(BaseModel):
    text: str
    rich_text_nodes: List[DynamicDataItemsModulesModuleDynamicDescRichTextNodes]


class DynamicDataItemsModulesModuleDynamicAdditional(BaseModel):
    common: Optional[Any] = Field(default=None)
    type: str
    # reserve: Any
    # goods: Any
    # vote: Any
    # ugc: Any


class DynamicDataItemsModulesModuleDynamicMajorUGCSeason(BaseModel):
    aid: int
    # badge: Any
    cover: str
    desc: str
    disable_preview: int
    duration_text: str
    jump_url: str
    # stat: Any
    title: str


class DynamicDataItemsModulesModuleDynamicMajorDrawItems(BaseModel):
    height: int
    size: int
    src: str
    tags: List[Any]
    width: int


class DynamicDataItemsModulesModuleDynamicMajorArticle(BaseModel):
    covers: List[str]
    desc: str
    id: int
    jump_url: str
    label: str
    title: str

class DynamicDataItemsModulesModuleDynamicMajorDrawItems(BaseModel):
    height: float
    size: float
    src: str

class DynamicDataItemsModulesModuleDynamicMajorDraw(BaseModel):
    id: int
    items: List[DynamicDataItemsModulesModuleDynamicMajorDrawItems]


class DynamicDataItemsModulesModuleDynamicMajorArchive(BaseModel):
    aid: str
    bvid: str
    cover: str
    desc: str
    disable_preview: int
    duration_text: str
    jump_url: str
    title: str
    type: int


class DynamicDataItemsModulesModuleDynamicMajorCommon(BaseModel):
    badge: Any
    biz_type: int
    cover: str
    desc: str
    id: str
    jump_url: str
    label: str
    sketch_id: str
    style: int
    title: str


class DynamicDataItemsModulesModuleDynamicMajorPgc(BaseModel):
    badge: Any
    cover: str
    epid: int
    jump_url: str
    season_id: int
    stat: Any
    sub_type: int
    title: str
    type: int


class DynamicDataItemsModulesModuleDynamicMajorLiveRcmd(BaseModel):
    content: str
    reserve_type: int


class DynamicDataItemsModulesModuleDynamicMajorMusic(BaseModel):
    cover: str
    id: int
    jump_url: str
    label: str
    title: str


class DynamicDataItemsModulesModuleDynamicMajorOpusSummary(BaseModel):
    rich_text_nodes: List[DynamicDataItemsModulesModuleDynamicDescRichTextNodes]
    text: str

class DynamicDataItemsModulesModuleDynamicMajorOpusPics(BaseModel):
    height: int
    width: int
    url: str
    size: float

class DynamicDataItemsModulesModuleDynamicMajorOpus(BaseModel):
    fold_action: List[Any]
    jump_url: str
    pics: List[DynamicDataItemsModulesModuleDynamicMajorOpusPics]
    summary: DynamicDataItemsModulesModuleDynamicMajorOpusSummary
    title: Union[None, str]
    # type: str


class DynamicDataItemsModulesModuleDynamicMajorLive(BaseModel):
    badge: Any
    cover: str
    desc_first: str
    desc_second: str
    id: int
    jump_url: str
    live_state: int
    reserve_type: int
    title: str


class DynamicDataItemsModulesModuleDynamicMajor(BaseModel):
    type: DynamicDataItemsMajorType
    ugc_season:Optional[DynamicDataItemsModulesModuleDynamicMajorUGCSeason] = Field(default=None)
    article: Optional[DynamicDataItemsModulesModuleDynamicMajorArticle] = Field(default=None)
    draw: Optional[DynamicDataItemsModulesModuleDynamicMajorDraw] = Field(default=None)
    archive: Optional[DynamicDataItemsModulesModuleDynamicMajorArchive] = Field(default=None)
    live_rcmd: Optional[DynamicDataItemsModulesModuleDynamicMajorLiveRcmd] = Field(default=None)
    common: Optional[DynamicDataItemsModulesModuleDynamicMajorCommon] = Field(default=None)
    pgc: Optional[DynamicDataItemsModulesModuleDynamicMajorPgc] = Field(default=None)
    # courses: Any
    music: Optional[DynamicDataItemsModulesModuleDynamicMajorMusic] = Field(default=None)
    opus: Optional[DynamicDataItemsModulesModuleDynamicMajorOpus] = Field(default=None)
    live: Optional[DynamicDataItemsModulesModuleDynamicMajorLive] = Field(default=None)
    # none: Any


class DynamicDataItemsModulesModuleDynamic(BaseModel):
    additional: Union[DynamicDataItemsModulesModuleDynamicAdditional, None]
    desc: Union[DynamicDataItemsModulesModuleDynamicDesc, None]
    major: Union[DynamicDataItemsModulesModuleDynamicMajor, None]
    # topic: Any


class DynamicDataItemsModules(BaseModel):
    module_author: DynamicDataItemsModulesModuleAuthor
    module_dynamic: DynamicDataItemsModulesModuleDynamic
    # module_more: Any
    # module_stat: Any
    # module_interaction: Any
    # module_fold: Any
    # module_dispute: Any
    # module_tag: Any


class DynamicDataItems(BaseModel):
    basic: DynamicDataItemsBasic
    id_str: str
    modules: DynamicDataItemsModules
    type: DynamicDataItemsType
    visible: bool
    

class DynamicDataItems(BaseModel):
    basic: DynamicDataItemsBasic
    id_str: str
    modules: DynamicDataItemsModules
    type: DynamicDataItemsType
    orig: Optional[DynamicDataItems] = Field(default=None)   # 仅动态类型为DYNAMIC_TYPE_FORWARD的情况下存在
    visible: bool
    
    
class DynamicData(BaseModel):
    has_more: bool
    items: List[DynamicDataItems]
    offset: str
    update_baseline: str
    update_num: int
