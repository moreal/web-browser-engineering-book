from dataclasses import dataclass
from typing import Literal


type Content = ImageContent | TextContent


class ContentFetcher:
    def __init__(self, connection_factory: ConnectionFactory = None):
        self.connection_factory = connection_factory


@dataclass(frozen=True)
class ImageContent:
    bytes: bytes
    media_type: Literal["image/jpeg", "image/png", "image/gif"]


@dataclass(frozen=True)
class TextContent:
    text: str
    media_type: Literal["text/plain", "text/html", "text/markdown"]
