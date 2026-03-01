from daiso_cli.models import ProductItem, SearchResponse

from .conftest import SAMPLE_PRODUCT_DOCUMENT


class TestProductItem:
    def test_parse_from_api_response(self) -> None:
        item = ProductItem.model_validate(SAMPLE_PRODUCT_DOCUMENT)

        assert item.product_number == "1056241"
        assert item.product_name == "개별 분리형 스탠드 7칸 약통"
        assert item.price == "2000"
        assert item.average_score == "4.8"
        assert item.review_count == "87"
        assert item.sold_out == "N"

    def test_detail_url(self) -> None:
        item = ProductItem(product_number="1056241")

        assert item.detail_url == ("https://www.daisomall.co.kr/pd/pdr/SCR_PDR_0001?pdNo=1056241")

    def test_full_image_url(self) -> None:
        item = ProductItem(product_image_url="/file/PD/test.jpg")

        assert item.full_image_url == "https://img.daisomall.co.kr/file/PD/test.jpg"

    def test_full_image_url_empty(self) -> None:
        item = ProductItem()

        assert item.full_image_url == ""

    def test_formatted_price(self) -> None:
        item = ProductItem(price="2000")

        assert item.formatted_price == "2,000원"

    def test_formatted_price_large(self) -> None:
        item = ProductItem(price="15000")

        assert item.formatted_price == "15,000원"

    def test_formatted_price_invalid(self) -> None:
        item = ProductItem(price="무료")

        assert item.formatted_price == "무료"

    def test_category(self) -> None:
        item = ProductItem(
            large_category_name="뷰티/위생",
            middle_category_name="가정의료용품",
            small_category_name="약통",
        )

        assert item.category == "뷰티/위생 > 가정의료용품 > 약통"

    def test_category_partial(self) -> None:
        item = ProductItem(large_category_name="뷰티/위생")

        assert item.category == "뷰티/위생"

    def test_category_empty(self) -> None:
        item = ProductItem()

        assert item.category == ""

    def test_default_values(self) -> None:
        item = ProductItem()

        assert item.product_number == ""
        assert item.product_name == ""
        assert item.price == ""
        assert item.sold_out == "N"
        assert item.new_product == "N"
        assert item.total_order_quantity == "0"


class TestSearchResponse:
    def test_default_values(self) -> None:
        response = SearchResponse()

        assert response.total_count == 0
        assert response.items == []

    def test_with_items(self) -> None:
        item = ProductItem(product_number="1", product_name="테스트")
        response = SearchResponse(total_count=1, items=[item])

        assert response.total_count == 1
        assert len(response.items) == 1
        assert response.items[0].product_name == "테스트"
