from truelove.db import FullMediaDataSchema


class DownloadException(Exception):
    def __init__(self, media: FullMediaDataSchema, message: str):
        self.media = media
        self.message = message
        super().__init__(
            f"{self.__class__.__name__}: {message} | Context: {media.platform} -> {media.author} -> {media.media_name}"
        )


class UnsupportedPlatformException(DownloadException):
    def __init__(self, media: FullMediaDataSchema):
        super().__init__(media, f"Unsupported platform: {media.platform}")


class CoreNotFoundException(DownloadException):
    def __init__(self, media: FullMediaDataSchema):
        super().__init__(media, f"Core {media.core} not found")


class UnsupportedMediaTypeException(DownloadException):
    def __init__(self, media: FullMediaDataSchema):
        super().__init__(media, f"Unsupported media type: {media.media_type}")


class DownloadFailedException(DownloadException):
    def __init__(self, media: FullMediaDataSchema, stderr):
        super().__init__(media, f"Download failed with error: {stderr}")
