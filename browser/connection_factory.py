from dataclasses import dataclass
from typing import Final

from .url import HttpFamilyUrl
from browser.connection import Connection, get_default_port


@dataclass(frozen=True, eq=True)
class ConnectionCacheKey:
    scheme: str
    host: str
    port: int


class ConnectionFactory:
    def __init__(self):
        self.connections: Final[dict[ConnectionCacheKey, Connection]] = {}

    def get(self, url: HttpFamilyUrl) -> Connection:
        cache_key = ConnectionCacheKey(
            scheme=url.scheme,
            host=url.host,
            port=url.port or get_default_port(url.scheme),
        )
        if (connection := self.connections.get(cache_key)) is not None:
            return connection

        connection = Connection(scheme=url.scheme, host=url.host, port=url.port)
        self.connections[cache_key] = connection
        return connection


GlobalConnectionFactory = ConnectionFactory()
