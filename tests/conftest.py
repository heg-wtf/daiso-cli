import pytest

from daiso_cli.models import ProductItem, SearchResponse

SAMPLE_PRODUCT_DOCUMENT = {
    "pdNo": "1056241",
    "pdNm": "개별 분리형 스탠드 7칸 약통",
    "exhPdNm": "개별 분리형 스탠드 7칸 약통",
    "pdPrc": "2000",
    "brndNm": "",
    "brndCd": "",
    "keywdCn": "약 소분,약통,개별 약통",
    "avgStscVal": "4.8",
    "revwCnt": "87",
    "newPdYn": "N",
    "massOrPsblYn": "Y",
    "pkupOrPsblYn": "Y",
    "totOrQy": "3529",
    "exhLargeCtgrNm": "뷰티/위생",
    "exhMiddleCtgrNm": "가정의료용품",
    "exhSmallCtgrNm": "약통",
    "pdImgUrl": "/file/PD/20250619/test.jpg",
    "soldOutYn": "N",
}

SAMPLE_SEARCH_API_RESPONSE = {
    "version": 43,
    "responseTime": "6 ms",
    "returnCode": 1,
    "status": 200,
    "resultSet": {
        "resultSize": 2,
        "errorCode": 0,
        "result": [
            {
                "errorCode": 0,
                "groupResult": [],
                "totalSize": 37,
                "realSize": 1,
            },
            {
                "errorCode": 0,
                "totalSize": 37,
                "realSize": 1,
                "resultDocuments": [SAMPLE_PRODUCT_DOCUMENT],
            },
        ],
    },
}

SAMPLE_EMPTY_SEARCH_RESPONSE = {
    "version": 43,
    "resultSet": {
        "result": [
            {"errorCode": 0, "totalSize": 0},
            {"errorCode": 0, "totalSize": 0, "resultDocuments": []},
        ],
    },
}


@pytest.fixture
def sample_product_item() -> ProductItem:
    return ProductItem.model_validate(SAMPLE_PRODUCT_DOCUMENT)


@pytest.fixture
def sample_search_response(sample_product_item: ProductItem) -> SearchResponse:
    return SearchResponse(total_count=37, items=[sample_product_item])
