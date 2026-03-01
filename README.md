# daiso-cli

다이소몰 상품 검색 CLI 도구

## 기술 스택

- **Python** 3.12+
- **Typer** - CLI 프레임워크
- **Scrapling** - HTTP 요청 (브라우저 TLS 핑거프린팅)
- **Pydantic** - 데이터 모델
- **Rich** - 터미널 출력 포맷팅

## 설치

```bash
uv sync
```

## 사용법

```bash
# 기본 검색 (테이블 출력)
daiso search "약통"

# 결과 수 지정
daiso search "텀블러" --count 10

# 페이지 이동
daiso search "접시" --page 2

# JSON 출력
daiso search "컵" --format json

# 마크다운 출력
daiso search "수납" --format markdown
```

### 옵션

| 옵션 | 단축 | 설명 | 기본값 |
|------|------|------|--------|
| `--count` | `-c` | 검색 결과 수 (1-100) | 30 |
| `--page` | `-p` | 페이지 번호 | 1 |
| `--sort` | `-s` | 정렬 기준 | (관련도순) |
| `--format` | `-f` | 출력 형식 (text/markdown/json) | text |

### 출력 형식

- **text** - Rich 테이블 (상품명, 가격, 평점, 리뷰, 카테고리, 품절여부, 링크)
- **markdown** - 마크다운 테이블
- **json** - JSON 구조화 데이터

## 프로젝트 구조

```
src/daiso_cli/
├── __init__.py          # 버전
├── main.py              # Typer CLI 진입점
├── client.py            # DaisoClient (Scrapling 기반)
├── models.py            # ProductItem, SearchResponse
└── commands/
    ├── __init__.py      # OutputFormat
    └── search.py        # search 커맨드
```

## 개발

```bash
# 테스트
uv run pytest -v

# 린트
uv run ruff check src/ tests/

# 포맷
uv run ruff format src/ tests/
```

## 라이선스

MIT
