import tkinter
from typing import Annotated
import typer

from browser.browser import Browser
from browser.url import Url

app = typer.Typer()


@app.command()
def main(
    url: Annotated[Url, typer.Argument(help="URL to open.", parser=Url.parse)],
):
    browser = Browser()
    browser.open(url)
    tkinter.mainloop()


if __name__ == "__main__":
    app()
