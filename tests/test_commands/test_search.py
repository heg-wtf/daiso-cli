from unittest.mock import MagicMock, patch

from typer.testing import CliRunner

from daiso_cli.client import DaisoApiError
from daiso_cli.main import app
from daiso_cli.models import ProductItem, SearchResponse

runner = CliRunner()


class TestSearchCommand:
    @patch("daiso_cli.commands.search.DaisoClient")
    def test_search_text_output(self, mock_client_class: MagicMock) -> None:
        result = SearchResponse(
            total_count=1,
            items=[
                ProductItem(
                    product_number="1056241",
                    product_name="개별 분리형 스탠드 7칸 약통",
                    price="2000",
                    average_score="4.8",
                    review_count="87",
                    large_category_name="뷰티/위생",
                    middle_category_name="가정의료용품",
                    small_category_name="약통",
                    sold_out="N",
                ),
            ],
        )
        mock_client_class.return_value.search_goods.return_value = result

        cli_result = runner.invoke(app, ["search", "약통"])

        assert cli_result.exit_code == 0
        assert "약통" in cli_result.output
        assert "SCR_PDR_0001?pdNo=1056241" in cli_result.output

    @patch("daiso_cli.commands.search.DaisoClient")
    def test_search_no_results(self, mock_client_class: MagicMock) -> None:
        mock_client_class.return_value.search_goods.return_value = SearchResponse()

        cli_result = runner.invoke(app, ["search", "없는상품"])

        assert cli_result.exit_code == 0
        assert "검색 결과가 없습니다" in cli_result.output

    @patch("daiso_cli.commands.search.DaisoClient")
    def test_search_json_output(self, mock_client_class: MagicMock) -> None:
        result = SearchResponse(
            total_count=1,
            items=[
                ProductItem(
                    product_number="1056241",
                    product_name="테스트 상품",
                    price="1000",
                ),
            ],
        )
        mock_client_class.return_value.search_goods.return_value = result

        cli_result = runner.invoke(app, ["search", "테스트", "--format", "json"])

        assert cli_result.exit_code == 0
        assert "테스트 상품" in cli_result.output
        assert "total_count" in cli_result.output

    @patch("daiso_cli.commands.search.DaisoClient")
    def test_search_markdown_output(self, mock_client_class: MagicMock) -> None:
        result = SearchResponse(
            total_count=1,
            items=[
                ProductItem(
                    product_number="1056241",
                    product_name="테스트 상품",
                    price="3000",
                    large_category_name="생활",
                ),
            ],
        )
        mock_client_class.return_value.search_goods.return_value = result

        cli_result = runner.invoke(app, ["search", "테스트", "--format", "markdown"])

        assert cli_result.exit_code == 0
        assert "검색 결과" in cli_result.output
        assert "테스트 상품" in cli_result.output
        assert "SCR_PDR_0001?pdNo=1056241" in cli_result.output

    @patch("daiso_cli.commands.search.DaisoClient")
    def test_search_api_error(self, mock_client_class: MagicMock) -> None:
        mock_client_class.return_value.search_goods.side_effect = DaisoApiError(500, "서버 오류")

        cli_result = runner.invoke(app, ["search", "약통"])

        assert cli_result.exit_code == 1
        assert "API 오류" in cli_result.output

    @patch("daiso_cli.commands.search.DaisoClient")
    def test_search_with_options(self, mock_client_class: MagicMock) -> None:
        mock_client_class.return_value.search_goods.return_value = SearchResponse()

        runner.invoke(app, ["search", "약통", "--count", "10", "--page", "2"])

        mock_client_class.return_value.search_goods.assert_called_once_with("약통", 10, 2, "")

    @patch("daiso_cli.commands.search.DaisoClient")
    def test_search_sold_out_item(self, mock_client_class: MagicMock) -> None:
        result = SearchResponse(
            total_count=1,
            items=[
                ProductItem(
                    product_number="999",
                    product_name="품절 상품",
                    price="1000",
                    sold_out="Y",
                ),
            ],
        )
        mock_client_class.return_value.search_goods.return_value = result

        cli_result = runner.invoke(app, ["search", "품절"])

        assert cli_result.exit_code == 0
        assert "SCR_PDR_0001?pdNo=999" in cli_result.output


class TestMainBanner:
    def test_no_subcommand_shows_banner(self) -> None:
        cli_result = runner.invoke(app, [])

        assert cli_result.exit_code == 0
        assert "Daiso" in cli_result.output
