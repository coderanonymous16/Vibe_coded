from __future__ import annotations

from app.ingestion.text_cleaner import clean_page_text


def chunk_text(text: str, chunk_size: int = 500, overlap: int = 80) -> list[str]:
    cleaned = clean_page_text(text)
    if not cleaned:
        return []
    chunks: list[str] = []
    start = 0
    while start < len(cleaned):
        end = min(len(cleaned), start + chunk_size)
        chunk = cleaned[start:end].strip()
        if chunk:
            chunks.append(chunk)
        if end == len(cleaned):
            break
        start = max(start + chunk_size - overlap, end - overlap)
    return chunks


def chunk_document_pages(pages: list[dict], chunk_size: int = 500, overlap: int = 80) -> list[dict]:
    chunks: list[dict] = []
    for page in pages:
        for index, chunk_text_value in enumerate(chunk_text(page["text"], chunk_size=chunk_size, overlap=overlap), start=1):
            chunks.append({
                "page": page["page_number"],
                "chunk_index": index,
                "text": chunk_text_value,
            })
    return chunks
