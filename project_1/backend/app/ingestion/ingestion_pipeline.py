from __future__ import annotations

from pathlib import Path

from app.ingestion.chunker import chunk_document_pages
from app.ingestion.metadata import DocumentMetadata
from app.ingestion.pdf_loader import load_pdf_reader
from app.ingestion.pdf_parser import extract_pages


def ingest_pdf(file_path: str | Path, metadata: DocumentMetadata, chunk_size: int = 500, overlap: int = 80) -> list[dict]:
    reader = load_pdf_reader(file_path)
    pages = extract_pages(reader)
    chunks = chunk_document_pages(pages, chunk_size=chunk_size, overlap=overlap)
    document_id = Path(str(file_path)).stem

    enriched: list[dict] = []
    for idx, chunk in enumerate(chunks, start=1):
        enriched.append({
            "chunk_id": f"{document_id}-chunk-{idx}",
            "document_id": document_id,
            "text": chunk["text"],
            "page": chunk["page"],
            "metadata": {
                **metadata.to_dict(),
                "chunk_index": chunk["chunk_index"],
            },
        })
    return enriched
