from typing import Literal
from browser.content import Content, HtmlContent
from browser.content_fetcher import fetch_content
from browser.renderer import _render_html_to_text

from .url import Url

import tkinter

from dataclasses import dataclass


@dataclass(frozen=True)
class BrowserOptions:
    http_version: Literal["1.0", "1.1"] = "1.0"


Position = tuple[int, int]
Element = tuple[Literal["text"], str] | tuple[Literal["box"], tuple[int, int]]
DisplayList = list[tuple[Position, Element]]


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
        self._current_display_list = self._get_display_list(self._current_content)
        self._render()

    def _display(self, display_list: DisplayList):
        self.canvas.delete("all")
        for (x, y), element in display_list:
            if y > self.scroll + self.height or y + self.VSTEP < self.scroll:
                continue
            match element:
                case ("text", text):
                    _ = self.canvas.create_text(x, y - self.scroll, text=text)
                case ("box", (width, height)):
                    _ = self.canvas.create_rectangle(
                        x, y - self.scroll, x + width, y - self.scroll + height
                    )

    def _get_display_list(self, content: Content) -> DisplayList:
        match content:
            case HtmlContent():
                text = _render_html_to_text(content)
                display_list: DisplayList = []
                cursor_x, cursor_y = self.HSTEP, self.VSTEP
                for c in text:
                    display_list.append(((cursor_x, cursor_y), ("text", c)))
                    cursor_x += self.HSTEP

                    if cursor_x >= self.width - self.HSTEP:
                        cursor_x = self.HSTEP
                        cursor_y += self.VSTEP

                return display_list
            case _:
                pass


def _get_max_height(display_list: DisplayList, vstep: int) -> int:
    return max(map(lambda x: x[0][1], display_list)) + vstep
