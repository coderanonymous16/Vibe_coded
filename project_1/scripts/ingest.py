#!/usr/bin/env python3
"""Simple ingestion helper script for local PDFs."""

from __future__ import annotations

import argparse
from pathlib import Path

from app.ingestion.ingestion_pipeline import ingest_pdf
from app.ingestion.metadata import DocumentMetadata


def main() -> None:
    parser = argparse.ArgumentParser(description="Ingest a PDF into ExamRAG chunks.")
    parser.add_argument("pdf_path", type=str, help="Path to the PDF file")
    parser.add_argument("--title", default="Academic Notes", help="Document title")
    parser.add_argument("--university", default="AKTU")
    parser.add_argument("--course", default="B.Tech CSE")
    parser.add_argument("--semester", type=int, default=6)
    parser.add_argument("--subject", default="DBMS")
    parser.add_argument("--unit", type=int, default=1)
    parser.add_argument("--chunk-size", type=int, default=500)
    parser.add_argument("--overlap", type=int, default=80)
    args = parser.parse_args()

    metadata = DocumentMetadata(
        title=args.title,
        university=args.university,
        course=args.course,
        semester=args.semester,
        subject=args.subject,
        unit=args.unit,
    )
    chunks = ingest_pdf(Path(args.pdf_path), metadata, chunk_size=args.chunk_size, overlap=args.overlap)
    print(f"Ingested {len(chunks)} chunks from {args.pdf_path}")
    for chunk in chunks[:3]:
        print(f"- {chunk['chunk_id']} :: {chunk['page']} :: {chunk['metadata']['subject']}")


if __name__ == "__main__":
    main()
