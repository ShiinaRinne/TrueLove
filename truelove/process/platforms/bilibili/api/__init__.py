import random
import aiohttp
from aiohttp.client_exceptions import ServerDisconnectedError

from typing import Literal, Any, List
from urllib.parse import urlencode


from truelove.config import config
from truelove.logger import logger
from .utils   import get_params
from .wbi     import get_signed_params
from .header  import Header
from .models  import AuthorInfo, AuthorVideoSearchInfo, VideoInfo

class BiliAPI:
    @staticmethod
    async def _request(url: str, method: Literal["GET", "POST"] = "GET", **kwargs: Any) -> dict:
        header = Header.new(cookie=config.cookie)
        signed_params = get_signed_params(kwargs.get("params", {}))
        req_url = f"{url}?{urlencode(signed_params)}"

        async with aiohttp.ClientSession() as session:
            try:
                proxies = random.choice(config.proxies) if config.proxies else None
                async with session.request(method=method, url=req_url, headers=header, proxy=proxies) as response:
                    res = await response.json()
                    if res is None or res["code"] != 0:
                        logger.error(f"url {url} 请求错误:\r\n {res}. \r\n headers: {header} \r\n params: {signed_params}")
                        raise RuntimeError(f"url {url} 请求错误:\r\n {res}. \r\n headers: {header} \r\n params: {signed_params}")
                    return res
            except ServerDisconnectedError as e:
                logger.error(f"url {url} 请求错误:\r\n {e}. \r\n headers: {header} \r\n params: {signed_params}")
                return None
        


    @staticmethod
    async def fetch_author_info(mid: int) -> AuthorInfo | None:
        """查询用户基础信息

        Args:
            mid (int): 用户mid

        Returns:
            UpInfo: _description_
        """
        url = "https://api.bilibili.com/x/space/wbi/acc/info"
        result = await BiliAPI._request(url, params=get_params(mid))
        
        return AuthorInfo.model_validate(result["data"])


    @staticmethod
    async def fetch_author_video_list(
        mid: int,
        ps: int = 30,
        tid: int = 0,
        pn: int = 1,
        order: Literal["pubdate", "click", "stow"] = "pubdate",
        keyword: str = "",
    ) -> AuthorVideoSearchInfo | None:
        """查询用户投稿视频明细

        Args:
            mid (int): 目标用户mid
            ps (int, optional): 每页项数. Defaults to 30.
            tid (int, optional): 筛选目标分区. Defaults to 0. 0: 不进行分区筛选. 分区tid为所筛选的分区
            pn (int, optional): 页码. Defaults to 1.
            order (Literal["pubdate", "click", "stow"], optional): 排序方式. 默认为pubdate. 最新发布: pubdate, 最多播放: click, 最多收藏: stow
            keyword (str, optional): 关键词筛选. 用于使用关键词搜索该UP主视频稿件.

        Returns:
            VideoSearchInfo: _description_
        """
        
        url = "https://api.bilibili.com/x/space/wbi/arc/search"
        result = await BiliAPI._request(url, params=get_params(mid, params={
            "ps": ps,
            "tid": tid,
            "pn": pn,
            "order": order,
            "keyword": keyword,
        }))
        return AuthorVideoSearchInfo.model_validate(result["data"])

    @staticmethod
    async def fetch_video_info(bvid: str) -> VideoInfo:
        query = {
            "bvid":bvid
        }
        url = f"https://api.bilibili.com/x/web-interface/view"
        result = await BiliAPI._request(url, params=query)
        
        return VideoInfo.model_validate(result["data"])
    

    
    
    
    