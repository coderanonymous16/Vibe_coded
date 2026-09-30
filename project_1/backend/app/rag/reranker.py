from __future__ import annotations


class Reranker:
    def rerank(self, results: list[dict]) -> list[dict]:
        reranked = []
        for item in results:
            metadata = item.get("metadata", {})
            boost = 0.0
            if metadata.get("subject"):
                boost += 0.2
            if metadata.get("unit") is not None:
                boost += 0.1
            item["score"] = item.get("score", 0.0) + boost
            reranked.append(item)
        reranked.sort(key=lambda item: item.get("score", 0.0), reverse=True)
        return reranked
