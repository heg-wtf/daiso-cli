import typer
from rich.console import Console

from daiso_cli.commands import search

app = typer.Typer(help="다이소몰 검색 CLI 도구", invoke_without_command=True)
console = Console()

app.command(name="search")(search.search)

BANNER = r"""
     ____        _             ____ _     ___
    |  _ \  __ _(_)___  ___   / ___| |   |_ _|
    | | | |/ _` | / __|/ _ \ | |   | |    | |
    | |_| | (_| | \__ \ (_) || |___| |___ | |
    |____/ \__,_|_|___/\___/  \____|_____|___|

    다이소몰 상품 검색 CLI 도구 (Daiso CLI)

    사용법: daiso search <검색어>
    도움말: daiso --help
"""


@app.callback()
def main(context: typer.Context) -> None:
    """다이소몰 상품 검색 CLI 도구."""
    if context.invoked_subcommand is None:
        console.print(BANNER)
        raise typer.Exit()
