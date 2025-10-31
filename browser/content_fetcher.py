from dataclasses import dataclass

from browser.handler import RedirectInfo
from browser.handler_factory import get_handler
from browser.url import Url
from browser.content import Content


@dataclass(frozen=True)
class ContentFetcher:
    def fetch(self, url: Url) -> Content:
        return self._handle(url)

    def _handle(self, url: Url, max_redirects: int = 20) -> Content:
        if max_redirects <= 0:
            raise ValueError("Max redirects exceeded")

        result = None
        while True:
            if (handler := get_handler(url.scheme)) is None:
                raise ValueError(f"Cannot handle {url}")

            result = handler.fetch(url)
            match result:
                case RedirectInfo():
                    return self._handle(result.url, max_redirects - 1)
                case _:
                    return result
