import tkinter
from dataclasses import dataclass
from typing import Literal, assert_never

from browser.content import Content, HtmlContent
from browser.content_fetcher import fetch_content
from browser.renderer import _render_html_to_text

from .url import Url


@dataclass(frozen=True)
class BrowserOptions:
    http_version: Literal["1.0", "1.1"] = "1.0"


Position = tuple[int, int]
TextElement = tuple[Literal["text"], str]
BoxElement = tuple[Literal["box"], tuple[int, int]]
Element = TextElement | BoxElement
DisplayList = list[tuple[Position, Element]]


HORIZONTAL_SCROLL_WIDTH = 10


class Browser:
    def __init__(
        self,
        height: int = 800,
        width: int = 600,
    ) -> None:
        self.height = height
        self.width = width
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

    def open(self, url: Url) -> None:
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
            self._current_content, width=self.width, hstep=self.HSTEP, vstep=self.VSTEP
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


def _get_display_list(
    content: Content, *, hstep: int, vstep: int, width: int
) -> DisplayList:
    match content:
        case HtmlContent():
            text = _render_html_to_text(content)
            display_list: DisplayList = []
            cursor_x, cursor_y = hstep, vstep
            for c in text:
                display_list.append(((cursor_x, cursor_y), ("text", c)))
                cursor_x += hstep

                if cursor_x >= width - hstep:
                    cursor_x = hstep
                    cursor_y += vstep

            return display_list
        case _:
            return []
