from __future__ import annotations

import math
import re


class BM25Retriever:
    def __init__(self, documents: list[str] | None = None):
        self.documents = documents or []
        self.doc_freqs: dict[str, int] = {}
        self.idf: dict[str, float] = {}
        self.doc_lens: list[int] = []
        self.avgdl = 0.0
        self._rebuild_index()

    def _tokenize(self, text: str) -> list[str]:
        return re.findall(r"\w+", text.lower())

    def _rebuild_index(self) -> None:
        self.doc_freqs = {}
        self.doc_lens = []
        for document in self.documents:
            tokens = self._tokenize(document)
            self.doc_lens.append(len(tokens))
            seen = set()
            for token in tokens:
                if token not in seen:
                    self.doc_freqs[token] = self.doc_freqs.get(token, 0) + 1
                    seen.add(token)
        self.avgdl = sum(self.doc_lens) / len(self.doc_lens) if self.doc_lens else 0.0
        total_docs = len(self.documents) or 1
        for token, freq in self.doc_freqs.items():
            self.idf[token] = math.log((total_docs - freq + 0.5) / (freq + 0.5) + 1.0)

    def index_documents(self, documents: list[str]) -> None:
        self.documents = documents
        self._rebuild_index()

    def search(self, query: str, top_k: int = 5, filters: dict | None = None) -> list[dict]:
        tokens = self._tokenize(query)
        if not tokens or not self.documents:
            return []
        scores: list[tuple[float, str]] = []
        for idx, document in enumerate(self.documents):
            if filters:
                metadata = {"text": document}
                for key, value in filters.items():
                    if metadata.get(key) != value and key not in document.lower():
                        break
            terms = self._tokenize(document)
            doc_len = len(terms) or 1
            score = 0.0
            term_counts = {}
            for token in terms:
                term_counts[token] = term_counts.get(token, 0) + 1
            for token in set(tokens):
                if token not in self.idf:
                    continue
                tf = term_counts.get(token, 0)
                score += self.idf[token] * ((tf * (1.5 + 1.0)) / (tf + 1.5 * (1 - 0.75 + 0.75 * (doc_len / self.avgdl if self.avgdl else 1))))
            scores.append((score, document))
        scores.sort(key=lambda item: item[0], reverse=True)
        return [{"score": score, "text": document} for score, document in scores[:top_k]]
