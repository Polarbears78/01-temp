#!/usr/bin/env python3
"""한글 문서(HWPX) 생성/편집 스크립트

사용법:
  새 문서 생성:  python3 write_hwpx.py create output.hwpx "제목" "본문1" "본문2" ...
  텍스트 치환:  python3 write_hwpx.py replace input.hwpx output.hwpx "찾을말" "바꿀말"
  문단 추가:    python3 write_hwpx.py append input.hwpx output.hwpx "추가할 문단1" "추가할 문단2" ...
  텍스트 추출:  python3 write_hwpx.py export input.hwpx [text|markdown|html]
"""

import sys
from hwpx import HwpxDocument


def create_document(output_path: str, paragraphs: list[str]):
    doc = HwpxDocument.new()
    for text in paragraphs:
        doc.add_paragraph(text)
    doc.save_to_path(output_path)
    print(f"문서 생성 완료: {output_path} ({len(paragraphs)}개 문단)")


def replace_text(input_path: str, output_path: str, old_text: str, new_text: str):
    doc = HwpxDocument.open(input_path)
    doc.replace_text_in_runs(old_text, new_text)
    doc.save_to_path(output_path)
    print(f"치환 완료: '{old_text}' → '{new_text}' → {output_path}")


def append_paragraphs(input_path: str, output_path: str, paragraphs: list[str]):
    doc = HwpxDocument.open(input_path)
    for text in paragraphs:
        doc.add_paragraph(text)
    doc.save_to_path(output_path)
    print(f"문단 추가 완료: {len(paragraphs)}개 → {output_path}")


def export_text(input_path: str, fmt: str = "text"):
    doc = HwpxDocument.open(input_path)
    if fmt == "markdown":
        print(doc.export_rich_markdown())
    elif fmt == "html":
        print(doc.export_html())
    else:
        print(doc.export_text())


def main():
    if len(sys.argv) < 2:
        print(__doc__)
        sys.exit(1)

    command = sys.argv[1]

    if command == "create" and len(sys.argv) >= 4:
        create_document(sys.argv[2], sys.argv[3:])

    elif command == "replace" and len(sys.argv) == 6:
        replace_text(sys.argv[2], sys.argv[3], sys.argv[4], sys.argv[5])

    elif command == "append" and len(sys.argv) >= 5:
        append_paragraphs(sys.argv[2], sys.argv[3], sys.argv[4:])

    elif command == "export" and len(sys.argv) >= 3:
        fmt = sys.argv[3] if len(sys.argv) > 3 else "text"
        export_text(sys.argv[2], fmt)

    else:
        print(__doc__)
        sys.exit(1)


if __name__ == "__main__":
    main()
