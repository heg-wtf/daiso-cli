# 아키텍처

## 개요

다이소몰 검색 API를 Scrapling으로 호출하여 터미널에 출력하는 CLI 도구.

## 데이터 흐름

```
사용자 입력 (검색어)
    ↓
[main.py] Typer CLI 파싱
    ↓
[commands/search.py] search 함수
    ↓
[client.py] DaisoClient.search_goods()
    ↓
[Scrapling Fetcher] HTTP GET → 다이소몰 API
    ↓
response.json() → dict 파싱
    ↓
[models.py] ProductItem.model_validate() → SearchResponse
    ↓
[commands/search.py] 출력 (text / markdown / json)
```

## API 엔드포인트

- **URL**: `https://www.daisomall.co.kr/ssn/search/SearchGoods`
- **메서드**: GET
- **주요 파라미터**: `searchTerm`, `pageNum`, `cntPerPage`, `searchSort`, `isCategory`
- **응답**: `resultSet.result[1].resultDocuments` (상품 배열), `resultSet.result[1].totalSize` (전체 건수)

## 상품 데이터 필드 매핑

| API 필드 | 모델 필드 | 설명 |
|----------|-----------|------|
| pdNo | product_number | 상품 번호 |
| pdNm | product_name | 상품명 |
| pdPrc | price | 가격 (문자열) |
| brndNm | brand_name | 브랜드명 |
| avgStscVal | average_score | 평균 평점 |
| revwCnt | review_count | 리뷰 수 |
| exhLargeCtgrNm | large_category_name | 대분류 |
| exhMiddleCtgrNm | middle_category_name | 중분류 |
| exhSmallCtgrNm | small_category_name | 소분류 |
| pdImgUrl | product_image_url | 이미지 경로 |
| soldOutYn | sold_out | 품절 여부 (Y/N) |
| newPdYn | new_product | 신상품 여부 (Y/N) |

## 의존성

| 패키지 | 용도 |
|--------|------|
| typer | CLI 프레임워크 |
| scrapling[fetchers] | HTTP 요청 (curl_cffi 기반 브라우저 핑거프린팅) |
| pydantic | 데이터 모델, API 응답 검증 |
| rich | 테이블 출력, 컬러 포맷팅 |
