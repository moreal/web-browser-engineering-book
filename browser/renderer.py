import abc
from typing import override

from .content import Content, TextContent, ImageContent


class Renderer[Output = str](abc.ABC):
    def __init__(self) -> None:
        pass

    @abc.abstractmethod
    def render(self, content: Content) -> Output:
        raise NotImplementedError


class ConsoleRenderer(Renderer[None]):
    def __init__(self) -> None:
        super().__init__()

    @override
    def render(self, content: Content) -> None:
        match content:
            case TextContent():
                print(content.text)
            case ImageContent():
                print("image content is not supported yet.")
