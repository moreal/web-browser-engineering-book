from typing import Literal, Optional
from browser.content_fetcher import ContentFetcher
from browser.renderer import Renderer
from browser.tab import Tab
from .cache import HttpCache
from .url import Url

from dataclasses import dataclass


@dataclass(frozen=True)
class BrowserOptions:
    http_version: Literal["1.0", "1.1"] = "1.0"


class Browser:
    cache: HttpCache
    renderer: Renderer
    content_fetcher: ContentFetcher

    def __init__(
        self,
        cache: HttpCache,
        renderer: Renderer,
        browser_options: Optional[BrowserOptions] = None,
    ) -> None:
        self.cache = cache
        self.renderer = renderer
        self.tabs = []

    def open(self, url: Url) -> Tab:
        content = self.cache.get(url)
        if content is None:
            content = self.renderer.render(url)
            self.cache.set(url, content)
        self.renderer.display(content)
