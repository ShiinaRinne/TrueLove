from pydantic import BaseModel
from typing import Any, List, Dict, Optional
from enum import Enum

    

# 获取视频详细信息(web端)
# https://api.bilibili.com/x/web-interface/view

# 请求方式：GET

# 认证方式：Cookie(SESSDATA)

# 限制游客访问的视频需要登录

# url参数：

# 参数名	类型	内容	必要性	备注
# aid	num	稿件avid	必要(可选)	avid与bvid任选一个
# bvid	str	稿件bvid	必要(可选)	avid与bvid任选一个
# json回复：

# 根对象：

# 字段	类型	内容	备注
# code	num	返回值	0：成功
# -400：请求错误
# -403：权限不足
# -404：无视频
# 62002：稿件不可见
# 62004：稿件审核中
# message	str	错误信息	默认为0
# ttl	num	1	
# data	obj	信息本体	
# data对象：

# 字段	类型	内容	备注
# bvid	str	稿件bvid	
# aid	num	稿件avid	
# videos	num	稿件分P总数	默认为1
# tid	num	分区tid	
# tname	str	子分区名称	
# copyright	num	视频类型	1：原创
# 2：转载
# pic	str	稿件封面图片url	
# title	str	稿件标题	
# pubdate	num	稿件发布时间	秒级时间戳
# ctime	num	用户投稿时间	秒级时间戳
# desc	str	视频简介	
# desc_v2	array	新版视频简介	
# state	num	视频状态	详情见属性数据文档
# attribute(已经弃用)	num	稿件属性位配置	详情见属性数据文档
# duration	num	稿件总时长(所有分P)	单位为秒
# forward	num	撞车视频跳转avid	仅撞车视频存在此字段
# mission_id	num	稿件参与的活动id	
# redirect_url	str	重定向url	仅番剧或影视视频存在此字段
# 用于番剧&影视的av/bv->ep
# rights	obj	视频属性标志	
# owner	obj	视频UP主信息	
# stat	obj	视频状态数	
# dynamic	str	视频同步发布的的动态的文字内容	
# cid	num	视频1P cid	
# dimension	obj	视频1P分辨率	
# premiere		null	
# teenage_mode	num		
# is_chargeable_season	bool		
# is_story	bool		
# no_cache	bool		作用尚不明确
# pages	array	视频分P列表	
# subtitle	obj	视频CC字幕信息	
# staff	array	合作成员列表	非合作视频无此项
# is_season_display	bool		
# user_garb	obj	用户装扮信息	
# honor_reply	obj		
# like_icon	str		
# argue_info	obj	争议/警告信息	


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

# subtitle对象：

# 字段	类型	内容	备注
# allow_submit	bool	是否允许提交字幕	
# list	array	字幕列表	
# subtitle对象中的list数组：

# 项	类型	内容	备注
# 0	obj	字幕1	
# n	obj	字幕(n+1)	
# ……	obj	……	……
# list数组中的对象：

# 字段	类型	内容	备注
# id	num	字幕id	
# lan	str	字幕语言	
# lan_doc	str	字幕语言名称	
# is_lock	bool	是否锁定	
# author_mid	num	字幕上传者mid	
# subtitle_url	str	json格式字幕文件url	
# author	obj	字幕上传者信息	
# list数组中的对象中的author对象：

# 字段	类型	内容	备注
# mid	num	字幕上传者mid	
# name	str	字幕上传者昵称	
# sex	str	字幕上传者性别	男 女 保密
# face	str	字幕上传者头像url	
# sign	str	字幕上传者签名	
# rank	num	10000	作用尚不明确
# birthday	num	0	作用尚不明确
# is_fake_account	num	0	作用尚不明确
# is_deleted	num	0	作用尚不明确
# staff数组：

# 项	类型	内容	备注
# 0	obj	合作成员1	
# n	obj	合作成员(n+1)	
# ……	obj	……	……
# staff数组中的对象：

# 字段	类型	内容	备注
# mid	num	成员mid	
# title	str	成员名称	
# name	str	成员昵称	
# face	str	成员头像url	
# vip	obj	成员大会员状态	
# official	obj	成员认证信息	
# follower	num	成员粉丝数	
# label_style	num		
# staff数组中的对象中的vip对象：

# 字段	类型	内容	备注
# type	num	成员会员类型	0：无
# 1：月会员
# 2：年会员
# status	num	会员状态	0：无
# 1：有
# theme_type	num	0	
# staff数组中的对象中的official对象：

# 字段	类型	内容	备注
# role	num	成员认证级别	见用户认证类型一览
# title	str	成员认证名	无为空
# desc	str	成员认证备注	无为空
# type	num	成员认证类型	-1：无
# 0：有
# data中的user_garb对象：

# 字段	类型	内容	备注
# url_image_ani_cut	str	某url？	
# data中的honor_reply对象：

# 字段	类型	内容	备注
# honor	array		
# honor数组中的对象：

# 字段	类型	内容	备注
# aid	num	当前稿件aid	
# type	num	1：入站必刷收录
# 2：第?期每周必看
# 3：全站排行榜最高第?名
# 4：热门	
# desc	num	描述	
# weekly_recommend_num	num		
# data中的argue_info对象：

# 字段	类型	内容	备注
# argue_link	str		作用尚不明确
# argue_msg	str	警告/争议提示信息	
# argue_type	int		作用尚不明确