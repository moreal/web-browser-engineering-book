import pathlib
import tkinter
from dataclasses import dataclass
from typing import Literal, assert_never

from browser.content import Content, HtmlContent
from browser.content_fetcher import fetch_content
from browser.renderer import _render_html_to_text

from .url import AboutUrl, Url, UrlParseError


@dataclass(frozen=True)
class BrowserOptions:
    http_version: Literal["1.0", "1.1"] = "1.0"


Position = tuple[int, int]
TextElement = tuple[Literal["text"], str]
BoxElement = tuple[Literal["box"], tuple[int, int]]
# "image", <path>, <size>
ImageElement = tuple[Literal["image"], str, tuple[int, int]]
Element = TextElement | BoxElement | ImageElement
DisplayList = list[tuple[Position, Element]]


HORIZONTAL_SCROLL_WIDTH = 10


class Browser:
    def __init__(self, height: int = 800, width: int = 600, rtl: bool = False) -> None:
        self.height = height
        self.width = width
        self.rtl = rtl
        self.HSTEP, self.VSTEP = 13, 18

        self.window = tkinter.Tk()
        self.canvas = tkinter.Canvas(self.window, height=self.height, width=self.width)
        self.canvas.pack(fill=tkinter.BOTH, expand=True)

        self.scroll = 0

        self._bind_events()
        self._current_content: Content | None = None
        self._current_display_list: DisplayList = []

    def _bind_events(self):
        self.window.bind("<Down>", self._scrolldown)
        self.window.bind("<Up>", self._scrollup)
        self.window.bind("<MouseWheel>", self._mousewheel)
        self.window.bind("<Button-4>", self._scrollup)
        self.window.bind("<Button-5>", self._scrollup)
        self.window.bind("<Configure>", self._configure)

    def _scrolldown(self, event):
        self._update_scroll(100)

    def _scrollup(self, event):
        self._update_scroll(-100)

    def _mousewheel(self, event: tkinter.Event):
        # FIXME: care cross platform (Windows, macOS, Linux)
        self._update_scroll(event.delta)

    def _configure(self, event: tkinter.Event):
        self.height = event.height
        self.width = event.width
        self._update_display_list()

    def _update_scroll(self, delta: int):
        max_height = _get_max_height(self._current_display_list, self.VSTEP)
        self.scroll = max(min(self.scroll + delta, max_height - self.height), 0)
        self._update_display_list()

    def open(self, url: str | Url) -> None:
        self.update_content(fetch_content(url))

    def _render(self):
        match self._current_content:
            case HtmlContent():
                self._display(self._current_display_list)
            case _:
                pass

    def update_content(self, content: Content):
        self._current_content = content
        self._update_display_list()

    def _update_display_list(self):
        assert self._current_content is not None
        display_list = _get_display_list(
            self._current_content,
            width=self.width,
            hstep=self.HSTEP,
            vstep=self.VSTEP,
            rtl=self.rtl,
        )
        if (
            vertical_scroll_bar := _get_vertical_scroll_bar(
                display_list,
                scroll=self.scroll,
                width=self.width,
                vstep=self.VSTEP,
                height=self.height,
            )
        ) is not None:
            display_list.append(vertical_scroll_bar)

        self._current_display_list = display_list
        self._render()

    def _display(self, display_list: DisplayList):
        self.canvas.delete("all")
        for (x, y), element in display_list:
            if y > self.scroll + self.height:
                continue
            match element:
                case ("text", text):
                    _ = self.canvas.create_text(x, y - self.scroll, text=text)
                case ("image", path, size):
                    image = _load_image(path)

                    _ = self.canvas.create_image(
                        x, y - self.scroll, image=image, anchor="nw"
                    )
                case ("box", (width, height)):
                    _ = self.canvas.create_rectangle(
                        x,
                        y,
                        x + width,
                        y + height,
                        fill="gray",
                    )


def _get_max_height(display_list: DisplayList, vstep: int) -> int:
    return max(map(lambda x: x[0][1], display_list)) + vstep


def _get_vertical_scroll_bar(
    display_list: DisplayList, *, scroll: int, width: int, height: int, vstep: int
) -> tuple[Position, BoxElement] | None:
    max_height = _get_max_height(display_list, vstep)

    if max_height <= height:
        return None

    rate = height / max_height
    vertical_scroll_length = int(height * rate)
    scroll_y = int(scroll * rate)
    return (width - HORIZONTAL_SCROLL_WIDTH, scroll_y), (
        "box",
        (HORIZONTAL_SCROLL_WIDTH, vertical_scroll_length),
    )


_image_cache: dict[str, tkinter.PhotoImage] = {}


def _load_image(path: str) -> tkinter.PhotoImage:
    if path not in _image_cache:
        _image_cache[path] = tkinter.PhotoImage(file=path)
    return _image_cache[path]


def _get_display_list(
    content: Content, *, hstep: int, vstep: int, width: int, rtl: bool = False
) -> DisplayList:
    match content:
        case HtmlContent():
            text = _render_html_to_text(content)
            display_list: DisplayList = []
            cursor_x, cursor_y = (hstep, 0) if rtl else (width - hstep, 0)
            iterator = _TextIterator(text)
            for typ, c in iterator:
                if c == "\n":
                    if rtl:
                        cursor_x = width - hstep
                    else:
                        cursor_x = hstep
                    cursor_y += vstep
                else:
                    if typ == "emoji":
                        display_list.append(
                            (
                                (cursor_x, cursor_y),
                                ("image", str(_to_emoji_filepath(c)), (0, 0)),
                            )
                        )
                    else:
                        display_list.append(((cursor_x, cursor_y), ("text", c)))
                    cursor_x += hstep if not rtl else -hstep

                if (not rtl and cursor_x >= width - hstep) or (
                    rtl and cursor_x < hstep
                ):
                    cursor_x = hstep if not rtl else width - hstep
                    cursor_y += vstep

            return display_list
        case _:
            return []


_OPENMOJI_BASE_PATH = pathlib.Path("data/openmoji")


# Make iterator receives string and
class _TextIterator:
    def __init__(self, text: str):
        self.text = text
        self.index = 0

    def __iter__(self):
        return self

    def __next__(self) -> tuple[Literal["text", "emoji"], str]:
        if self.index >= len(self.text):
            raise StopIteration

        for i in range(10, 0, -1):
            if _exist_emoji(self.text[self.index : self.index + i]):
                char = self.text[self.index : self.index + i]
                self.index += i
                return ("emoji", char)

        char = self.text[self.index]
        self.index += 1
        return ("text", char)


def _to_emoji_filename(s: str) -> str:
    return f"{'-'.join((hex(ord(c))[2:] for c in s))}.png"


def _to_emoji_filepath(s: str) -> pathlib.Path:
    return _OPENMOJI_BASE_PATH.joinpath(_to_emoji_filename(s)).absolute()


def _exist_emoji(s: str) -> bool:
    pathval = _to_emoji_filepath(s)
    retval = pathval.exists()
    return retval
