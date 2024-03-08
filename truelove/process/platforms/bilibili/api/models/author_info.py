from enum import Enum
from pydantic import BaseModel
from typing import Any, List, Optional



# 用户基础信息
class AuthorInfo(BaseModel):
    face: str
    mid: int
    name: str


# =================================
# 用户投稿视频明细
class AuthorVideoSearchVList(BaseModel):
    aid: int  # 稿件avid
    author: str  # 视频UP主, 不一定为目标用户（合作视频）
    bvid: str  # 稿件bvid
    created: int  # 投稿时间
    description: str  # 视频简介. 从这个列表里获取到的简介有最大长度限制
    length: str  # 视频长度 MM:SS
    mid: int  # 视频UP主mid, 不一定为目标用户（合作视频）
    pic: str  # 视频封面
    title: str  # 视频标题
    typeid: int  # 视频分区tid

    # meta:     dict # 似乎是合集？ 没数据时为 null


class AuthorVideoSearchPage(BaseModel):
    count: int
    pn: int
    ps: int


class AuthorVideoSearchList(BaseModel):
    slist: List[Any]
    # tlist: List[Any] # 投稿视频分区索引
    vlist: List[AuthorVideoSearchVList]


class AuthorVideoSearchInfo(BaseModel):
    gaia_data: Any
    gaia_res_type: int
    is_risk: bool
    list: AuthorVideoSearchList
    page: AuthorVideoSearchPage


# =================================


# =================================
# 用户动态
class AuthorSpaceInfoItemBasic(BaseModel):
    comment_id_str: str
    comment_type: int
    rid_str: str


class AuthorSpaceInfoItemModuleAuthorPubAction(Enum):
    POST_VIDEO = "投稿了视频"
    LIVE = "直播了"
    POST_ARTICLE = "投稿了文章"
    POST_ARCHIVE = "更新了合集"
    POST_WITH_OTHERS = "与他人联合创作"
    POST_DYNAMIC_VIDEO = "发布了动态视频"
    POST_LIVE_RECORD = "投稿了直播回放"


class AuthorSpaceInfoItemModuleAuthor(BaseModel):
    # avatar: Dict[Any, Any]
    # decorate: Dict[Any, Any]
    face: str
    jump_url: str
    label: str
    mid: int
    name: str
    pub_action: AuthorSpaceInfoItemModuleAuthorPubAction
    pub_location_text: str
    pub_time: str
    pub_ts: int
    type: str  # https://github.com/SocialSisterYi/bilibili-API-collect/blob/29da46295bfe4992ada9106a1147db92659927f8/docs/dynamic/dynamic_enum.md#%E4%BD%9C%E8%80%85%E7%B1%BB%E5%9E%8B


class AuthorSpaceInfoItemModuleDynamicDescRichTextNodes(BaseModel):
    jump_url: Optional[str]
    orig_text: str  # 原始文本
    text: str  # 替换后的文本
    type: str  # https://github.com/SocialSisterYi/bilibili-API-collect/blob/29da46295bfe4992ada9106a1147db92659927f8/docs/dynamic/dynamic_enum.md#%E5%AF%8C%E6%96%87%E6%9C%AC%E8%8A%82%E7%82%B9%E7%B1%BB%E5%9E%8B
    # emoji: Any
    # rid: str # 关联id
    # goods: Any # 商品信息


class AuthorSpaceInfoItemModuleDynamicDesc(BaseModel):
    text: str  # 动态的文字内容
    rich_text_nodes: List[AuthorSpaceInfoItemModuleDynamicDescRichTextNodes]  # 富文本节点列表


class AuthorSpaceInfoItemModuleDynamicMajorArchive(BaseModel):
    aid: str
    bvid: str
    cover: str
    desc: str
    disable_preview: int
    duration_text: str
    jump_url: str
    title: str
    type: int


# https://github.com/SocialSisterYi/bilibili-API-collect/blob/29da46295bfe4992ada9106a1147db92659927f8/docs/dynamic/all.md#data%E5%AF%B9%E8%B1%A1---items%E6%95%B0%E7%BB%84%E4%B8%AD%E7%9A%84%E5%AF%B9%E8%B1%A1---modules%E5%AF%B9%E8%B1%A1---module_dynamic%E5%AF%B9%E8%B1%A1---major%E5%AF%B9%E8%B1%A1
# 似乎有好几个是可选的
class AuthorSpaceInfoItemModuleDynamicMajor(BaseModel):
    archive: AuthorSpaceInfoItemModuleDynamicMajorArchive  # 视频信息
    type: str  # 动态主体类型 https://github.com/SocialSisterYi/bilibili-API-collect/blob/29da46295bfe4992ada9106a1147db92659927f8/docs/dynamic/dynamic_enum.md#%E5%8A%A8%E6%80%81%E4%B8%BB%E4%BD%93%E7%B1%BB%E5%9E%8B
    article: Any  # 专栏类型
    draw: Any  # 带图动态
    live_rcmd: Any  # 直播状态
    common: Any  # 一般类型
    music: Any  # 音频信息
    opus: Any  # 图文动态
    # live: Any # 不知道
    none: Any  # 动态失效 MAJOR_TYPE_NONE


# https://github.com/SocialSisterYi/bilibili-API-collect/blob/29da46295bfe4992ada9106a1147db92659927f8/docs/dynamic/all.md#data%E5%AF%B9%E8%B1%A1---items%E6%95%B0%E7%BB%84%E4%B8%AD%E7%9A%84%E5%AF%B9%E8%B1%A1---modules%E5%AF%B9%E8%B1%A1---module_dynamic%E5%AF%B9%E8%B1%A1
class AuthorSpaceInfoItemModuleDynamic(BaseModel):
    additional: Any
    desc: AuthorSpaceInfoItemModuleDynamicDesc | None  # 其他动态时为null. 什么是其他动态？
    mahor: AuthorSpaceInfoItemModuleDynamicMajor | None  # 转发动态时为null
    topic: Any


class AuthorSpaceInfoItemModules(BaseModel):
    """
    module_author: UP主信息
    module_dynamic: 动态内容信息

    """

    module_author: AuthorSpaceInfoItemModuleAuthor
    module_dynamic: AuthorSpaceInfoItemModuleDynamic
    # module_more: Dict[Any, Any]
    # module_stat: Dict[Any, Any]


class AuthorSpaceInfoItem(BaseModel):
    # basic: Dict[Any, Any]
    id_str: str
    modules: AuthorSpaceInfoItemModules
    type: str
    visible: bool


class AuthorSpaceInfo(BaseModel):
    has_more: bool
    items: List[AuthorSpaceInfoItem]
    offset: str
    update_baseline: str
    update_num: int
