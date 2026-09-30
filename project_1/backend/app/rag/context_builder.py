from __future__ import annotations


def build_context(chunks: list[dict]) -> str:
    if not chunks:
        return "No relevant context found in the academic sources."
    snippets = []
    for chunk in chunks:
        text = chunk.get("text", "")
        metadata = chunk.get("metadata", {})
        if metadata:
            snippets.append(f"Source: {metadata.get('title', 'Unknown')} | Page {chunk.get('page', 'n/a')}\n{text}")
        else:
            snippets.append(text)
    return "\n\n---\n\n".join(snippets)
