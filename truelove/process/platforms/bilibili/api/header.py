class Header:
    @classmethod
    def new(cls, cookie: str) -> dict:
        return {
            "User-Agent": "Mozilla/5.0",
            "Origin": "https://space.bilibili.com",
            "Referer": "https://space.bilibili.com",
            "Cookie": cookie,
            "Accept": "*/*",
            "authority": "api.bilibili.com"
        }

