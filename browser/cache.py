import abc

from .url import Url
from .content import Content


class Cache(abc.ABC):
    @abc.abstractmethod
    def get(self, url: Url) -> Content:
        raise NotImplementedError()

    @abc.abstractmethod
    def set(self, url: Url, content: Content):
        raise NotImplementedError()
