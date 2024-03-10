from truelove.db import FullVideoDataSchema


class DownloadException(Exception):
    def __init__(self, video: FullVideoDataSchema, message: str):
        self.video = video
        self.message = message
        super().__init__(
            f"{self.__class__.__name__}: {message} | Context: {video.platform} -> {video.author} -> {video.video_name}"
        )


class UnsupportedPlatformException(DownloadException):
    def __init__(self, video: FullVideoDataSchema):
        super().__init__(video, f"Unsupported platform: {video.platform}")


class CoreNotFoundException(DownloadException):
    def __init__(self, video: FullVideoDataSchema):
        super().__init__(video, f"Core {video.core} not found")
        
class PlatformNotFoundException(DownloadException):
    def __init__(self, msg: str):
        super().__init__(msg)

class DownloadFailedException(DownloadException):
    def __init__(self, video: FullVideoDataSchema, stderr):
        super().__init__(video, f"Download failed with error: {stderr}")
