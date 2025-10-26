from .protocols.connection_factory import ConnectionFactory
from .cache import Cache
from .url import Url
from .content import Content


class ContentFetcher:
    def __init__(self, cache: Cache, connection_factory: ConnectionFactory):
        self.cache = cache
        self.connection_factory = connection_factory

    def fetch(self, url: Url) -> Content:
        connection = self.connection_factory.get(url)
        response = connection.request("GET", url)
        return Content(response.status_code, response.headers, response.body)
