from typing import Annotated
import typer

from browser.content_fetcher import fetch_content
from browser.url import Url
from browser.renderer import ConsoleRenderer

app = typer.Typer()


@app.command()
def main(
    url: Annotated[Url, typer.Argument(help="URL to open.", parser=Url.parse)],
):
    content = fetch_content(url)
    renderer = ConsoleRenderer()
    renderer.render(content)


if __name__ == "__main__":
    app()
