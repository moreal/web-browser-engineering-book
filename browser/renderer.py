import abc
import tkinter
from typing import override

from .content import Content, HtmlContent, ImageContent, PlainTextContent, ViewSource


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
            case HtmlContent():
                _render_html_to_text(content)
            case ViewSource():
                print("In view-source mode:")
                print(_get_raw(content.content))
            case ImageContent():
                print("image content is not supported yet.")
            case PlainTextContent():
                print(content.text)
            case _:
                print("unknown content type")


def _get_raw(content: Content) -> str:
    match content:
        case HtmlContent():
            return content.data.decode("utf-8")  # FIXME: get charset
        case ImageContent():
            return "Image: " + content.bytes.hex()
        case PlainTextContent():
            return content.text
        case _:
            return ""


def _render_html_to_text(content: HtmlContent) -> str:
    import re

    data = content.data.decode("utf-8")  # FIXME: get charset
    data = re.sub(r"<[^>]*>", "", data)  # Remove XML tags
    return data.replace("&lt;", "<").replace("&gt;", ">")
