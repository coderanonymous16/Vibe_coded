from __future__ import annotations

import re


def normalize_whitespace(text: str) -> str:
    text = text.replace("\r\n", "\n")
    text = re.sub(r"\s+", " ", text).strip()
    return text


def clean_page_text(text: str) -> str:
    text = text.replace("\xa0", " ")
    return normalize_whitespace(text)
