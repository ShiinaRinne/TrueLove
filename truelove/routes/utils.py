from typing import List, Any, Union
from urllib.parse import urlparse

def parse_uid(url: Union[str, None]) -> str | None:
    if url is None: return None
    url = str(url)
    if url.startswith("https://space.bilibili.com"):
        return urlparse(url).path.split("/")[1]
    return url

