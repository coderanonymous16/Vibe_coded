from __future__ import annotations

from pypdf import PdfReader


def extract_pages(reader: PdfReader) -> list[dict]:
    pages: list[dict] = []
    for page_number, page in enumerate(reader.pages, start=1):
        text = page.extract_text() or ""
        pages.append({"page_number": page_number, "text": text})
    return pages
