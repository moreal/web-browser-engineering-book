from typing import Annotated
import typer

from browser.url import Url
from browser.tab import Tab

app = typer.Typer()


@app.command()
def main(
    url: Annotated[Url, typer.Argument(help="URL to open.", parser=Url.parse)],
):
    tab = Tab.open(url)
    print(tab.body)


if __name__ == "__main__":
    app()
