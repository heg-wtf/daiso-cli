import json
from typing import Annotated

import typer
from rich.console import Console
from rich.table import Table

from daiso_cli.client import DaisoApiError, DaisoClient
from daiso_cli.commands import OutputFormat
from daiso_cli.models import SearchResponse

console = Console()


def _print_as_text(query: str, result: SearchResponse) -> None:
    table = Table(title=f"'{query}' 검색 결과 (총 {result.total_count}건)")
    table.add_column("상품명", style="bold cyan", max_width=40)
    table.add_column("가격", style="green", justify="right")
    table.add_column("평점", style="yellow", justify="center")
    table.add_column("리뷰", justify="right")
    table.add_column("카테고리", style="dim")
    table.add_column("품절", justify="center")
    table.add_column("링크", style="dim", no_wrap=True)

    for item in result.items:
        sold_out_mark = "Y" if item.sold_out == "Y" else ""
        table.add_row(
            item.product_name,
            item.formatted_price,
            item.average_score or "-",
            item.review_count or "0",
            item.category,
            sold_out_mark,
            item.detail_url,
        )

    console.print(table)


def _print_as_markdown(query: str, result: SearchResponse) -> None:
    console.print(f"### '{query}' 검색 결과 (총 {result.total_count}건)\n")
    console.print("| 상품명 | 가격 | 평점 | 리뷰 | 카테고리 | URL |")
    console.print("|--------|------|------|------|----------|-----|")
    for item in result.items:
        console.print(
            f"| {item.product_name} | {item.formatted_price} | "
            f"{item.average_score or '-'} | {item.review_count or '0'} | "
            f"{item.category} | [링크]({item.detail_url}) |"
        )


def _print_as_json(result: SearchResponse) -> None:
    data = {
        "total_count": result.total_count,
        "items": [
            {
                "product_number": item.product_number,
                "product_name": item.product_name,
                "price": item.price,
                "formatted_price": item.formatted_price,
                "brand_name": item.brand_name,
                "average_score": item.average_score,
                "review_count": item.review_count,
                "category": item.category,
                "sold_out": item.sold_out == "Y",
                "detail_url": item.detail_url,
                "image_url": item.full_image_url,
            }
            for item in result.items
        ],
    }
    console.print(json.dumps(data, ensure_ascii=False, indent=2))


def search(
    query: Annotated[str, typer.Argument(help="검색어")],
    count: Annotated[int, typer.Option("--count", "-c", help="검색 결과 수 (1-100)")] = 30,
    page: Annotated[int, typer.Option("--page", "-p", help="페이지 번호")] = 1,
    sort: Annotated[str, typer.Option("--sort", "-s", help="정렬 기준")] = "",
    output_format: Annotated[
        OutputFormat, typer.Option("--format", "-f", help="출력 형식")
    ] = OutputFormat.TEXT,
) -> None:
    """다이소몰 상품을 검색합니다."""
    client = DaisoClient()

    try:
        result = client.search_goods(query, count, page, sort)
    except DaisoApiError as error:
        console.print(f"[red]API 오류: {error}[/red]")
        raise typer.Exit(code=1) from error

    if not result.items:
        console.print("[yellow]검색 결과가 없습니다.[/yellow]")
        return

    match output_format:
        case OutputFormat.TEXT:
            _print_as_text(query, result)
        case OutputFormat.MARKDOWN:
            _print_as_markdown(query, result)
        case OutputFormat.JSON:
            _print_as_json(result)
