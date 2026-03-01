# daiso-cli

다이소몰 상품 검색 CLI 도구.

## 프로젝트 컨텍스트

- 다이소몰 검색 API (`/ssn/search/SearchGoods`)를 Scrapling Fetcher로 호출
- 응답은 `response.json()` 메서드로 파싱 (Scrapling의 `.text`는 HTML 파서를 거치므로 사용하지 않음)
- API 응답 구조: `resultSet.result[1].resultDocuments`에 상품 목록, `totalSize`에 전체 건수
- 상품 상세 URL: `https://www.daisomall.co.kr/pd/pdr/SCR_PDR_0001?pdNo={pdNo}`

## 주요 명령어

```bash
uv sync                        # 의존성 설치
uv run pytest -v               # 테스트 실행
uv run ruff check src/ tests/  # 린트
uv run ruff format src/ tests/ # 포맷
uv run daiso search "검색어"   # 실행
```

## 코드 구조

- `src/daiso_cli/main.py` - Typer 앱, 배너, 커맨드 등록
- `src/daiso_cli/client.py` - DaisoClient, DaisoApiError, Scrapling Fetcher 호출
- `src/daiso_cli/models.py` - ProductItem (Pydantic, alias 매핑), SearchResponse
- `src/daiso_cli/commands/search.py` - search 함수, 3가지 출력 포맷 (text/markdown/json)
- `src/daiso_cli/commands/__init__.py` - OutputFormat StrEnum

## 개발 규칙

- Scrapling 로그 억제: `logging.getLogger("scrapling").setLevel(logging.WARNING)`
- ProductItem 필드는 API 응답 키를 Pydantic alias로 매핑
- 테스트에서 Scrapling Fetcher는 `@patch("daiso_cli.client.Fetcher")`로 mock
- mock 응답은 `.json()` 메서드를 mock: `mock_response.json.return_value = {...}`
