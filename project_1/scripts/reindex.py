#!/usr/bin/env python3
"""Utility to rebuild the in-memory retrieval index for local development."""

from __future__ import annotations

import json
from pathlib import Path

from app.rag.retriever import Retriever


def build_index(folder: str = "data") -> Retriever:
    base = Path(__file__).resolve().parents[1]
    data_dir = base / folder
    chunks = []
    for json_path in data_dir.glob("*.json"):
        payload = json.loads(json_path.read_text(encoding="utf-8"))
        if isinstance(payload, list):
            chunks.extend(payload)
    retriever = Retriever(chunks)
    print(f"Loaded {len(chunks)} chunks into the retriever from {data_dir}")
    return retriever


if __name__ == "__main__":
    build_index()
