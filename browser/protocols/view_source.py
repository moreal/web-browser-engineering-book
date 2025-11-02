from dataclasses import dataclass
from typing import Callable, override
from browser.content import Content, ViewSource
from browser.handler import UrlHandler
from browser.url import Url


__all__ = ("ViewSourceUrlHandler",)


@dataclass(frozen=True)
class ViewSourceUrlHandler(UrlHandler):
    content_fetcher: Callable[[Url], Content]

    @override
    def fetch(self, url: Url):
        if url.path is None:
            raise ValueError("Invalid URL. view-source: scheme needs path")
        content = self.content_fetcher(Url.parse(url.path))
        return ViewSource(content=content)
