from __future__ import annotations

from pathlib import Path

from pypdf import PdfReader


def load_pdf_bytes(file_path: str | Path) -> bytes:
    path = Path(file_path)
    return path.read_bytes()


def load_pdf_reader(file_path: str | Path) -> PdfReader:
    return PdfReader(str(file_path))
