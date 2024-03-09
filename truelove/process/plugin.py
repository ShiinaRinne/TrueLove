from truelove.logger import logger
from truelove.process.event import tl_event
from truelove.process.utils import run_in_executor
from truelove.db.models.schema import FullMediaDataSchema


@tl_event("before_download")
async def before_download(t: FullMediaDataSchema) -> tuple:
    
    return (t,), {}

@tl_event("after_download")
async def after_download(t: FullMediaDataSchema):
    # await example_convert_mp4_to_mp3(t)
    
    pass
    

async def example_convert_mp4_to_mp3(t: FullMediaDataSchema):
    if t.media_type == "video":
        import os
        files = os.listdir(t.download_path)
        files = [f for f in files if os.path.isfile(os.path.join(t.download_path, f)) and f.startswith(f)]
        for f in files: 
            params = ["ffmpeg", "-i", os.path.join(t.download_path, f), "-vn", "-acodec", "libmp3lame", "-y", os.path.join(t.download_path, f"{os.path.splitext(f)[0]}.mp3")]
            result = await run_in_executor(params)
            if result.returncode != 0:
                logger.error(f"convert {t.media_name} to mp3 failed")
        logger.info(f"convert {t.media_name} to mp3 success")