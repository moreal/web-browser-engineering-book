from dataclasses import dataclass
from browser.content import Content
from browser.content_fetcher import GlobalContentFetcher
from browser.url import Url


@dataclass(frozen=True)
class Tab:
    url: Url
    content: Content

    @staticmethod
    def open(url: Url) -> "Tab":
        content = GlobalContentFetcher.fetch(url)

        return Tab(url=url, content=content)
