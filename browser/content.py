from dataclasses import dataclass
from typing import Literal

__all__ = (
    "Content",
    "ImageContent",
    "UnknownContent",
    "PlainTextContent",
    "HtmlContent",
)


type Content = (
    ImageContent | UnknownContent | UnhandledContent | PlainTextContent | HtmlContent
)


@dataclass(frozen=True)
class ImageContent:
    bytes: bytes
    media_type: Literal["image/jpeg", "image/png", "image/gif"]


@dataclass(frozen=True)
class UnknownContent:
    bytes: bytes
    media_type: None


@dataclass(frozen=True)
class UnhandledContent:
    bytes: bytes
    media_type: str


@dataclass(frozen=True)
class PlainTextContent:
    text: str
    media_type: Literal["text/plain"] = "text/plain"


@dataclass(frozen=True)
class HtmlContent:
    data: bytes
    media_type: Literal["text/html"] = "text/html"


def recognize_content(media_type: str, data: bytes) -> Content:
    match media_type:
        case "text/html":
            return HtmlContent(data)
        case "image/jpeg":
            return ImageContent(media_type=media_type, bytes=data)
        case _:
            return UnhandledContent(media_type=media_type, bytes=data)
