import time
from typing import Final, Protocol

from browser.protocols.http.response import HttpResponse

from .url import HttpFamilyUrl


class HttpCache(Protocol):
    """
    Protocol to cache only HTTP/S responses (not other schemes like file:, data:).
    """

    def get(self, url: HttpFamilyUrl) -> HttpResponse | None: ...

    def set(self, url: HttpFamilyUrl, response: HttpResponse, expires: int) -> None: ...


class MemoryCache(HttpCache):
    def __init__(self):
        self._cache: Final = dict[HttpFamilyUrl, tuple[HttpResponse, int]]()

    def get(self, url: HttpFamilyUrl) -> HttpResponse | None:
        if (cached := self._cache.get(url)) is None:
            return None
        response, expire_at = cached
        if expire_at < time.time():
            _ = self._cache.pop(url)
            return None
        return response

    def set(self, url: HttpFamilyUrl, response: HttpResponse, expires: int) -> None:
        self._cache[url] = (response, expires)
