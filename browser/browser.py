import enum
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
        self.HEIGHT = height
        self.WIDTH = width
        self.VSTEP, self.HSTEP = 13, 18

        self.window = tkinter.Tk()
        self.canvas = tkinter.Canvas(self.window, height=self.HEIGHT, width=self.WIDTH)
        self.canvas.pack()

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

    def _scrolldown(self, event):
        self._update_scroll(self.scroll + 100)

    def _scrollup(self, event):
        self._update_scroll(max(self.scroll - 100, 0))

    def _mousewheel(self, event: tkinter.Event):
        self._update_scroll(max(self.scroll - event.delta, 0))

    def _update_scroll(self, new_scroll: int):
        self.scroll = new_scroll
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
            if y > self.scroll + self.HEIGHT or y + self.VSTEP < self.scroll:
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
                HSTEP, VSTEP = 13, 18
                cursor_x, cursor_y = HSTEP, VSTEP
                for c in text:
                    display_list.append(((cursor_x, cursor_y), ("text", c)))
                    cursor_x += HSTEP

                    if cursor_x >= self.WIDTH - HSTEP:
                        cursor_x = HSTEP
                        cursor_y += VSTEP

                return display_list
            case _:
                pass
