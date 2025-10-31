from dataclasses import dataclass

from browser.handler import RedirectInfo
from browser.handler_factory import GlobalHandlerFactory, HandlerFactory
from .url import Url, to_concrete
from .content import Content


@dataclass(frozen=True)
class ContentFetcher:
    handler_factory: HandlerFactory = GlobalHandlerFactory

    def fetch(self, url: Url) -> Content:
        return self._handle(url)

    def _handle(self, url: Url, max_redirects: int = 20) -> Content:
        if max_redirects <= 0:
            raise ValueError("Max redirects exceeded")

        concrete_url = to_concrete(url)
        result = None
        while True:
            handler = self.handler_factory.get(concrete_url)
            result = handler.fetch(concrete_url)
            match result:
                case RedirectInfo():
                    return self._handle(result.url, max_redirects - 1)
                case _:
                    return result


GlobalContentFetcher = ContentFetcher()
