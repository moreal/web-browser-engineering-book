import abc

from .content import Content, TextContent, ImageContent


class Renderer[Output = str](abc.ABC):
    def __init__(self) -> None:
        pass

    def render(self, content: Content) -> Output:
        raise NotImplementedError


class TextRenderer(Renderer[str]):
    def __init__(self) -> None:
        super().__init__()

    def render(self, content: Content) -> str:
        match content:
            case TextContent():
                print(content.text)
            case ImageContent():
                print("image content is not supported yet.")
