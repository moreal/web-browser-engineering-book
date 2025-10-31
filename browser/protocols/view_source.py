from dataclasses import dataclass
from typing import override
from browser.content import ViewSource
from browser.content_fetcher import ContentFetcher
from browser.handler import UrlHandler
from browser.url import Url


__all__ = ("ViewSourceUrlHandler",)


@dataclass(frozen=True)
class ViewSourceUrlHandler(UrlHandler):
    content_fetcher: ContentFetcher

    @override
    def fetch(self, url: Url):
        if url.path is None:
            raise ValueError("Invalid URL. view-source: scheme needs path")
        content = self.content_fetcher.fetch(Url.parse(url.path))
        return ViewSource(content=content)
