#!/usr/bin/env python3
"""한글 문서(HWP/HWPX) 텍스트 추출 스크립트"""

import sys
import os
import zipfile
import xml.etree.ElementTree as ET
import olefile


def read_hwp(filepath: str) -> str:
    """HWP(바이너리) 파일에서 텍스트를 추출합니다."""
    if not olefile.isOleFile(filepath):
        raise ValueError(f"유효한 HWP 파일이 아닙니다: {filepath}")

    ole = olefile.OleFileIO(filepath)

    # PrvText 스트림에서 미리보기 텍스트 추출
    if ole.exists("PrvText"):
        data = ole.openstream("PrvText").read()
        text = data.decode("utf-16-le", errors="replace")
        ole.close()
        return text.strip()

    # PrvText가 없으면 BodyText 섹션에서 추출 시도
    sections = []
    for stream in ole.listdir():
        path = "/".join(stream)
        if path.startswith("BodyText/Section"):
            raw = ole.openstream(stream).read()
            # BodyText는 바이너리 포맷이므로 간단한 텍스트 추출
            decoded = raw.decode("utf-16-le", errors="replace")
            # 제어 문자 제거 후 읽을 수 있는 텍스트만 추출
            cleaned = "".join(ch for ch in decoded if ch.isprintable() or ch in "\n\r\t")
            sections.append(cleaned)

    ole.close()

    if sections:
        return "\n".join(sections)

    raise ValueError("텍스트를 추출할 수 없습니다.")


def read_hwpx(filepath: str) -> str:
    """HWPX(XML 기반) 파일에서 텍스트를 추출합니다."""
    if not zipfile.is_zipfile(filepath):
        raise ValueError(f"유효한 HWPX 파일이 아닙니다: {filepath}")

    texts = []
    with zipfile.ZipFile(filepath, "r") as zf:
        # Contents 폴더 안의 section XML 파일들을 찾아 파싱
        section_files = sorted(
            name for name in zf.namelist()
            if name.startswith("Contents/") and name.endswith(".xml")
            and "section" in name.lower()
        )

        if not section_files:
            # section 파일이 없으면 모든 XML에서 텍스트 추출 시도
            section_files = sorted(
                name for name in zf.namelist()
                if name.startswith("Contents/") and name.endswith(".xml")
            )

        for section_file in section_files:
            xml_data = zf.read(section_file)
            root = ET.fromstring(xml_data)
            # 모든 텍스트 노드 추출
            for elem in root.iter():
                if elem.text and elem.text.strip():
                    texts.append(elem.text.strip())
                if elem.tail and elem.tail.strip():
                    texts.append(elem.tail.strip())

    if not texts:
        raise ValueError("텍스트를 추출할 수 없습니다.")

    return "\n".join(texts)


def read_document(filepath: str) -> str:
    """파일 확장자에 따라 HWP 또는 HWPX 문서를 읽습니다."""
    if not os.path.exists(filepath):
        raise FileNotFoundError(f"파일을 찾을 수 없습니다: {filepath}")

    ext = os.path.splitext(filepath)[1].lower()

    if ext == ".hwp":
        return read_hwp(filepath)
    elif ext == ".hwpx":
        return read_hwpx(filepath)
    else:
        # 확장자가 없으면 파일 시그니처로 판별
        if olefile.isOleFile(filepath):
            return read_hwp(filepath)
        elif zipfile.is_zipfile(filepath):
            return read_hwpx(filepath)
        else:
            raise ValueError(f"지원하지 않는 파일 형식입니다: {ext}")


def main():
    if len(sys.argv) < 2:
        print("사용법: python3 read_hwp.py <파일경로.hwp|.hwpx>")
        sys.exit(1)

    filepath = sys.argv[1]
    try:
        text = read_document(filepath)
        print(text)
    except (ValueError, FileNotFoundError) as e:
        print(f"오류: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
