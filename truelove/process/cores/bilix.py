from .basecore import BaseCore
from truelove.db.models.schema import WatcheeSchema, VideoSchema, FullVideoDataSchema
from truelove.config import config
from truelove.logger import logger
from truelove.process.utils import run_in_executor


class Bilix(BaseCore):
    def __init__(self):
        super().__init__()
        self.name = "bilix"
        self.author = "HFrost0"
        self.license = "Apache-2.0"
        
    async def download_video(self, md: FullVideoDataSchema):
        if md.platform != "bilibili":
            raise Exception(f"Unknown exception: {md}")
        
        for i in range(1, md.video_num + 1):
            video_id_with_p = f"{md.video_id}?p={i}"
            md2 = md.model_copy(update={"video_id": video_id_with_p})
            await self.__download_video_by_id(md2)
    
    async def __download_video_by_id(self, md: FullVideoDataSchema):
        download_url = f"https://www.bilibili.com/video/{md.video_id}"
        cmd = "bilix" # install bilix with pip, no need to use absolute path
        params = [
            str(cmd),
            "v",  download_url,
            "-d", md.download_path,
        ]
            
        if config.cookie != "":     params.extend(["--cookie", config.cookie])
        if config.cover:            params.append("--image")
        if config.subtitle:         params.append("--subtitle")
        if config.dm:               params.append("--dm")
             
        logger.info(f"Download {md.platform} -> {md.author} -> {md.video_name} started")
        
        result = await run_in_executor(params)
        logger.info("Output:", result)

        return "Download completed."