from typing import Annotated
import typer

from browser.url import URL
from browser.tab import Tab

app = typer.Typer()


@app.command()
def main(
    url: Annotated[URL, typer.Argument(help="URL to open.", parser=URL.parse)],
):
    tab = Tab.open(url)
    print(tab.body)


if __name__ == "__main__":
    app()
