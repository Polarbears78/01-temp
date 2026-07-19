---
name: hwpx-edit
description: 한글 문서(HWPX)를 읽고, 생성하고, 편집하는 스킬. 한글 문서 작성/수정/텍스트 추출 요청 시 사용.
trigger: hwpx, hwp, 한글 문서, 한글 파일, 공문서, 보고서 작성, 문서 생성, 문서 편집
---

# HWPX 문서 편집 스킬

한글 문서(.hwpx)를 한컴오피스 없이 Python으로 읽고, 생성하고, 편집합니다.
`python-hwpx` 라이브러리와 `olefile`을 사용합니다.

## 의존성

```bash
pip install python-hwpx olefile
```

## 의사결정 트리

사용자 요청을 아래 카테고리로 분류한 뒤 해당 워크플로를 따릅니다:

1. **읽기/추출** → 기존 문서에서 텍스트, 표, 이미지 추출
2. **새 문서 생성** → 빈 문서에서 시작하여 내용 구성
3. **기존 문서 편집** → 텍스트 치환, 문단 추가, 서식 변경
4. **양식 채우기** → 템플릿의 필드를 데이터로 채움

---

## 1. 읽기/추출

### HWP (바이너리) 파일 읽기

```python
# read_hwp.py 스크립트 사용
python3 read_hwp.py 문서.hwp
```

### HWPX 파일 읽기

```python
from hwpx import HwpxDocument

doc = HwpxDocument.open("문서.hwpx")

# 평문 텍스트 추출
text = doc.export_text()

# 마크다운으로 변환 (서식 보존)
md = doc.export_rich_markdown()

# HTML 변환
html = doc.export_html()
```

---

## 2. 새 문서 생성

```python
from hwpx import HwpxDocument

doc = HwpxDocument.new()

# 문단 추가
doc.add_paragraph("제목입니다")
doc.add_paragraph("본문 내용입니다.")
doc.add_paragraph("")  # 빈 줄

# 저장
doc.save_to_path("새문서.hwpx")
```

### 서식이 있는 문서 생성 예시

```python
from hwpx import HwpxDocument

doc = HwpxDocument.new()

# 제목
doc.add_paragraph("2026년 업무 보고서")

# 본문
doc.add_paragraph("1. 개요")
doc.add_paragraph("본 보고서는 2026년 상반기 업무 실적을 정리한 문서입니다.")
doc.add_paragraph("")
doc.add_paragraph("2. 주요 성과")
doc.add_paragraph("- 매출 전년 대비 15% 증가")
doc.add_paragraph("- 신규 고객 200건 확보")
doc.add_paragraph("")
doc.add_paragraph("3. 향후 계획")
doc.add_paragraph("하반기에는 해외 시장 진출을 본격적으로 추진합니다.")

doc.save_to_path("업무보고서.hwpx")
```

---

## 3. 기존 문서 편집

### 텍스트 치환

```python
from hwpx import HwpxDocument

doc = HwpxDocument.open("원본.hwpx")

# 단순 텍스트 치환
doc.replace_text_in_runs("임시", "확정")

# 색상 지정하여 치환 (빨간색)
doc.replace_text_in_runs("초안", "최종본", text_color="#FF0000")

doc.save_to_path("수정본.hwpx")
```

### 문단 추가

```python
doc = HwpxDocument.open("기존문서.hwpx")
doc.add_paragraph("추가된 문단입니다.")
doc.save_to_path("기존문서-수정.hwpx")
```

---

## 4. 양식 채우기

```python
from hwpx import HwpxDocument

doc = HwpxDocument.open("신청서.hwpx")

result = doc.fill_by_path({
    "성명 > right": "홍길동",
    "소속 > right": "개발팀",
    "연락처 > right": "010-1234-5678",
    "신청일 > right": "2026-07-19",
})

doc.save_to_path("신청서-완료.hwpx")
```

---

## 주의사항

- **HWP(바이너리)** 파일은 읽기만 가능합니다. 편집/생성은 HWPX만 지원합니다.
- 저장 시 원본을 덮어쓰지 않도록 별도 파일명을 사용하세요.
- 대용량 문서는 처리 시간이 길어질 수 있습니다.
- `python-hwpx`는 Python 3.10 이상이 필요합니다.

## 프로젝트 내 도구

| 파일 | 용도 |
|------|------|
| `read_hwp.py` | HWP/HWPX 텍스트 추출 CLI |
| `.claude/skills/hwpx-edit.md` | 이 스킬 파일 |
