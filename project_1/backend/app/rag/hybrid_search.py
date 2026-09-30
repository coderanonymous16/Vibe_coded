from __future__ import annotations


def fuse_results(vector_hits: list[dict], bm25_hits: list[dict], alpha: float = 0.5) -> list[dict]:
    merged: dict[str, dict] = {}
    for hit in vector_hits:
        key = hit.get("chunk_id") or hit.get("text")
        merged[key] = {**hit, "score": alpha * hit.get("score", 0.0)}
    for hit in bm25_hits:
        key = hit.get("chunk_id") or hit.get("text")
        item = merged.get(key, {**hit, "score": 0.0})
        item["score"] += (1 - alpha) * hit.get("score", 0.0)
        merged[key] = item
    return sorted(merged.values(), key=lambda item: item["score"], reverse=True)
