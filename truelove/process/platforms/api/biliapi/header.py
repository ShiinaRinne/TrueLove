from requests import session
from urllib.parse import urlencode
import time

from .wbi import get_signed_params


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

session = session()

proxies = {
    "http": "http://localhost:10809",
}

def test():
    cookie = "blackside_state=0; buvid_fp_plain=undefined; buvid3=A274C332-A51B-4774-88A2-A85B497736F7167647infoc; buvid4=2835E8D1-BDAE-B602-F179-1D5E72FB294334048-022012118-sUX1fLmKLX29A6fIo2XBAA%3D%3D; CURRENT_BLACKGAP=0; i-wanna-go-back=-1; LIVE_BUVID=AUTO6116321373836093; balh_is_closed=; balh_server_inner=__custom__; DedeUserID=251841982; DedeUserID__ckMd5=53fec7ee87acded9; header_theme_version=CLOSE; hit-new-style-dyn=1; CURRENT_PID=bd87df30-c884-11ed-87bc-a904b787ed07; balh_server_custom_hk=https://bili.yae.ac.cn; balh_remove_pre_ad=Y; balh_server_custom=https://bili.yae.ac.cn; FEED_LIVE_VERSION=V8; hit-dyn-v2=1; nostalgia_conf=-1; SESSDATA=282e2099%2C1706660581%2C01ddf%2A81; bili_jct=4427790e5f8fc279c13fa85aa0645423; b_ut=5; _uuid=7566ECAE-DC86-7163-6A1010-869614E1826530656infoc; enable_web_push=DISABLE; CURRENT_FNVAL=4048; b_nut=100; CURRENT_QUALITY=120; home_feed_column=5; fingerprint=88b83b1cd4c7cea40924ab44d9d9da01; rpdid=|(~Y||mR~uY0J'u~|JulRJkJ; browser_resolution=2072-1118; bp_t_offset_251841982=879090792331739174; buvid_fp=956927d4b5b66a82eb4b78836ef393ea; bili_ticket=eyJhbGciOiJIUzI1NiIsImtpZCI6InMwMyIsInR5cCI6IkpXVCJ9.eyJleHAiOjE3MDM5ODYyNTksImlhdCI6MTcwMzcyNjk5OSwicGx0IjotMX0.X9ePGURUsek-fr5W1ogIHyT3lL5XElcgbQiY1_ZZJ60; bili_ticket_expires=1703986199; sid=7ovscf69; b_lsid=6391BF62_18CB43C9EDD; PVID=1; PPA_CI=3db468ee81fa40c7a7fe6a27330a90e7"
    header = Header.new(cookie=cookie)

    url = "https://api.bilibili.com/x/space/wbi/acc/info"
    signed_params = get_signed_params(
        params={
            "mid": 512313464,
            "web_location": 1550101,
            "token": "",
            "platform": "web",
        }
    )
    # signed_params["w_rid"] = "616c38faaac3ecedaa1c213458f8275f"
    url = url + "?" + urlencode(signed_params)
    
    result = session.get(url=url, headers=header, proxies=proxies).text
    
    print(url)
    print(result)

