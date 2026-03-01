from pydantic import BaseModel, ConfigDict, Field


class ProductItem(BaseModel):
    """다이소몰 상품 정보."""

    model_config = ConfigDict(populate_by_name=True)

    product_number: str = Field(alias="pdNo", default="")
    product_name: str = Field(alias="pdNm", default="")
    price: str = Field(alias="pdPrc", default="")
    brand_name: str = Field(alias="brndNm", default="")
    average_score: str = Field(alias="avgStscVal", default="")
    review_count: str = Field(alias="revwCnt", default="")
    large_category_name: str = Field(alias="exhLargeCtgrNm", default="")
    middle_category_name: str = Field(alias="exhMiddleCtgrNm", default="")
    small_category_name: str = Field(alias="exhSmallCtgrNm", default="")
    product_image_url: str = Field(alias="pdImgUrl", default="")
    sold_out: str = Field(alias="soldOutYn", default="N")
    new_product: str = Field(alias="newPdYn", default="N")
    total_order_quantity: str = Field(alias="totOrQy", default="0")
    keyword_content: str = Field(alias="keywdCn", default="")

    @property
    def detail_url(self) -> str:
        return f"https://www.daisomall.co.kr/pd/pdr/SCR_PDR_0001?pdNo={self.product_number}"

    @property
    def full_image_url(self) -> str:
        if self.product_image_url:
            return f"https://img.daisomall.co.kr{self.product_image_url}"
        return ""

    @property
    def formatted_price(self) -> str:
        try:
            return f"{int(self.price):,}원"
        except ValueError:
            return self.price

    @property
    def category(self) -> str:
        parts = [self.large_category_name, self.middle_category_name, self.small_category_name]
        return " > ".join(part for part in parts if part)


class SearchResponse(BaseModel):
    """다이소몰 검색 응답."""

    total_count: int = 0
    items: list[ProductItem] = []
