import abc

from browser.content import Content


class Handler[TUrl](abc.ABC):
    @abc.abstractmethod
    def fetch(self, url: TUrl) -> Content:
        pass
