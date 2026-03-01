import logging
from urllib.parse import urlencode

from scrapling.fetchers import Fetcher

from daiso_cli.models import ProductItem, SearchResponse

logging.getLogger("scrapling").setLevel(logging.WARNING)


class DaisoApiError(Exception):
    """다이소몰 API 호출 실패 시 발생하는 예외."""

    def __init__(self, status_code: int, message: str) -> None:
        self.status_code = status_code
        self.message = message
        super().__init__(f"API 오류 (status={status_code}): {message}")


class DaisoClient:
    """다이소몰 검색 API 클라이언트 (Scrapling 기반)."""

    SEARCH_URL = "https://www.daisomall.co.kr/ssn/search/SearchGoods"

    def search_goods(
        self,
        query: str,
        count_per_page: int = 30,
        page_number: int = 1,
        search_sort: str = "",
    ) -> SearchResponse:
        """상품을 검색합니다.

        Args:
            query: 검색어
            count_per_page: 페이지당 결과 수 (1-100)
            page_number: 페이지 번호
            search_sort: 정렬 기준

        Returns:
            검색 결과

        Raises:
            DaisoApiError: API 호출 실패 시
        """
        parameters = {
            "searchTerm": query,
            "searchQuery": "",
            "pageNum": str(page_number),
            "brndCd": "",
            "cntPerPage": str(count_per_page),
            "userId": "",
            "newPdYn": "",
            "massOrPsblYn": "",
            "pkupOrPsblYn": "",
            "fdrmOrPsblYn": "",
            "quickOrPsblYn": "",
            "searchSort": search_sort,
            "isCategory": "1",
        }

        url = f"{self.SEARCH_URL}?{urlencode(parameters)}"

        try:
            response = Fetcher.get(url, stealthy_headers=True)
        except Exception as error:
            raise DaisoApiError(0, f"요청 실패: {error}") from error

        if response.status != 200:
            raise DaisoApiError(response.status, "검색 요청 실패")

        try:
            data = response.json()
        except Exception as error:
            raise DaisoApiError(response.status, f"응답 파싱 실패: {error}") from error

        return self._parse_response(data)

    def _parse_response(self, data: dict) -> SearchResponse:
        result_set = data.get("resultSet", {})
        results = result_set.get("result", [])

        if len(results) < 2:
            return SearchResponse()

        product_result = results[1]
        total_count = product_result.get("totalSize", 0)
        documents = product_result.get("resultDocuments", [])

        items = [ProductItem.model_validate(document) for document in documents]

        return SearchResponse(total_count=total_count, items=items)
