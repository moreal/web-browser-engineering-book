import abc
from dataclasses import dataclass

from browser.content import Content
from browser.url import Url


@dataclass(frozen=True)
class RedirectInfo:
    url: Url


class UrlHandler(abc.ABC):
    @abc.abstractmethod
    def fetch(self, url: Url) -> Content | RedirectInfo:
        pass
