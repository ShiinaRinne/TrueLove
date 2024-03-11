import os
import sys
import time
import string
import secrets
import asyncio
import subprocess
from typing import Literal

from truelove.config import config
from truelove.db.models import FullVideoDataSchema

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


def parse_save_dir(author: str, media_name: str, platform: str, watche_type: str):
    dir: str = config.save_dir
    media_name = media_name.replace("/", "-").replace("\\", "-").replace(":", "-").replace("*", "-").replace("?", "-").replace("\"", "-").replace("<", "-").replace(">", "-").replace("|", "-")
    replacements = {
        "{author}":                 author,
        "{filename}":               media_name,
        "{filename_without_ext}":   media_name.rsplit(".", 1)[0] if "." in media_name else "",
        "{ext}":                    media_name.rsplit(".", 1)[1] if "." in media_name else "",
        "{watch_type}":            watche_type,
        "{platform}":               platform,
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
        os.makedirs(dir, exist_ok=True)
    return dir


def parse_core_dir(platform: Literal["bilibili"]):
    if platform  == "bilibili":
        return config.root_dir / "bin/bilix"
    

def bili_source(bvid):
    return f"https://www.bilibili.com/video/{bvid}"
