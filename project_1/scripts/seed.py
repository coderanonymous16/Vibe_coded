#!/usr/bin/env python3
"""Seed a few sample academic documents for local development."""

from __future__ import annotations

from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DATA_DIR = ROOT / "data"


def seed_sample_documents() -> list[dict]:
    sample = [
        {
            "title": "DBMS Unit 3 Notes",
            "university": "AKTU",
            "course": "B.Tech CSE",
            "semester": 6,
            "subject": "DBMS",
            "unit": 3,
            "source": "sample",
        },
        {
            "title": "Operating Systems Quick Revision",
            "university": "AKTU",
            "course": "B.Tech CSE",
            "semester": 6,
            "subject": "OS",
            "unit": 2,
            "source": "sample",
        },
    ]
    DATA_DIR.mkdir(exist_ok=True)
    (DATA_DIR / "sample_documents.json").write_text(__import__("json").dumps(sample, indent=2), encoding="utf-8")
    return sample


if __name__ == "__main__":
    documents = seed_sample_documents()
    print(f"Seeded {len(documents)} sample documents into {DATA_DIR / 'sample_documents.json'}")
