import os
import sys
import time
import string
import secrets
import asyncio
import subprocess
from typing import Literal

from truelove.config import config
from truelove.db.models import FullMediaDataSchema

from concurrent.futures import ThreadPoolExecutor


async def run_in_executor(cmd):
    loop = asyncio.get_running_loop()
    with ThreadPoolExecutor() as executor:
        return await loop.run_in_executor(executor, subprocess.run, cmd)
    
    
async def sem_coro(sem, coro):
    async with sem:
        return await coro



def generate_random_string(length=16):
    characters = string.ascii_letters + string.digits
    random_string = "".join(secrets.choice(characters) for i in range(length))
    return random_string


def parse_save_dir(media: FullMediaDataSchema):
    dir: str = config.save_dir
    media_name = media.media_name.replace("/", "-").replace("\\", "-").replace(":", "-").replace("*", "-").replace("?", "-").replace("\"", "-").replace("<", "-").replace(">", "-").replace("|", "-")
    replacements = {
        "{author}":                 media.author,
        "{filename}":               media_name,
        "{filename_without_ext}":   media_name.rsplit(".", 1)[0] if "." in media.media_name else "",
        "{ext}":                    media_name.rsplit(".", 1)[1] if "." in media.media_name else "",
        "{platform}":               media.platform,
        "{timestamp}":              str(int(time.time())),
        "{timestamp_nano}":         str(time.time_ns()),
        "{datetime}":               time.strftime("%Y%m%d%H%M%S"),
        "{date}":                   time.strftime("%Y%m%d"),
        "{year}":                   time.strftime("%Y"),
        "{month}":                  time.strftime("%m"),
        "{day}":                    time.strftime("%d"),
        "{hour}":                   time.strftime("%H"),
        "{minute}":                 time.strftime("%M"),
        "{second}":                 time.strftime("%S"),
        "{randomkey16}":            generate_random_string(16),
        "{randomkey8}":             generate_random_string(8),
    }
    for k, v in replacements.items():
        dir = dir.replace(k, v)
    if os.path.exists(dir) is False:
        os.makedirs(dir)
    return dir


def parse_core_dir(platform: Literal["bilibili"]):
    if platform  == "bilibili":
        return config.root_dir / "bin/bilix"
    

def bili_source(bvid):
    return f"https://www.bilibili.com/video/{bvid}"
