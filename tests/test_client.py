from unittest.mock import MagicMock, patch

import pytest

from daiso_cli.client import DaisoApiError, DaisoClient

from .conftest import SAMPLE_EMPTY_SEARCH_RESPONSE, SAMPLE_SEARCH_API_RESPONSE


class TestDaisoClient:
    @patch("daiso_cli.client.Fetcher")
    def test_search_goods_success(self, mock_fetcher: MagicMock) -> None:
        mock_response = MagicMock()
        mock_response.status = 200
        mock_response.json.return_value = SAMPLE_SEARCH_API_RESPONSE
        mock_fetcher.get.return_value = mock_response

        client = DaisoClient()
        result = client.search_goods("약통")

        assert result.total_count == 37
        assert len(result.items) == 1
        assert result.items[0].product_name == "개별 분리형 스탠드 7칸 약통"
        assert result.items[0].price == "2000"

    @patch("daiso_cli.client.Fetcher")
    def test_search_goods_calls_fetcher_with_correct_url(self, mock_fetcher: MagicMock) -> None:
        mock_response = MagicMock()
        mock_response.status = 200
        mock_response.json.return_value = SAMPLE_EMPTY_SEARCH_RESPONSE
        mock_fetcher.get.return_value = mock_response

        client = DaisoClient()
        client.search_goods("약통", count_per_page=10, page_number=2)

        call_args = mock_fetcher.get.call_args
        url = call_args[0][0]
        assert "searchTerm=%EC%95%BD%ED%86%B5" in url
        assert "cntPerPage=10" in url
        assert "pageNum=2" in url

    @patch("daiso_cli.client.Fetcher")
    def test_search_goods_api_error(self, mock_fetcher: MagicMock) -> None:
        mock_response = MagicMock()
        mock_response.status = 500
        mock_fetcher.get.return_value = mock_response

        client = DaisoClient()
        with pytest.raises(DaisoApiError) as exception_information:
            client.search_goods("약통")

        assert exception_information.value.status_code == 500

    @patch("daiso_cli.client.Fetcher")
    def test_search_goods_network_error(self, mock_fetcher: MagicMock) -> None:
        mock_fetcher.get.side_effect = ConnectionError("네트워크 오류")

        client = DaisoClient()
        with pytest.raises(DaisoApiError) as exception_information:
            client.search_goods("약통")

        assert exception_information.value.status_code == 0

    @patch("daiso_cli.client.Fetcher")
    def test_search_goods_invalid_json(self, mock_fetcher: MagicMock) -> None:
        mock_response = MagicMock()
        mock_response.status = 200
        mock_response.json.side_effect = ValueError("invalid json")
        mock_fetcher.get.return_value = mock_response

        client = DaisoClient()
        with pytest.raises(DaisoApiError):
            client.search_goods("약통")

    @patch("daiso_cli.client.Fetcher")
    def test_search_goods_empty_result(self, mock_fetcher: MagicMock) -> None:
        mock_response = MagicMock()
        mock_response.status = 200
        mock_response.json.return_value = SAMPLE_EMPTY_SEARCH_RESPONSE
        mock_fetcher.get.return_value = mock_response

        client = DaisoClient()
        result = client.search_goods("없는상품")

        assert result.total_count == 0
        assert len(result.items) == 0

    def test_parse_response_insufficient_results(self) -> None:
        client = DaisoClient()
        result = client._parse_response({"resultSet": {"result": []}})

        assert result.total_count == 0
        assert len(result.items) == 0
