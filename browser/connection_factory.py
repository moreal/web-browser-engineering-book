from dataclasses import dataclass

from .url import Url
from .connection import Connection


@dataclass
class ConnectionData:
    scheme: str
    host: str
    port: int


class ConnectionFactory:
    def __init__(self):
        self.connections: dict[(str, int), Connection] =
    def get(url: Url) -> Connection:
        if url.startswith("http://"):
            return HTTPConnection(url)
        elif url.startswith("https://"):
            return HTTPSConnection(url)
        else:
            raise ValueError(f"Unsupported protocol: {url}")
