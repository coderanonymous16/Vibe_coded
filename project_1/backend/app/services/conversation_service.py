from __future__ import annotations

from collections import defaultdict

_CONVERSATIONS: dict[str, list[dict]] = defaultdict(list)


def create_conversation(user_id: str, title: str = "Untitled") -> dict:
    conversation_id = f"conv-{len(_CONVERSATIONS) + 1}"
    _CONVERSATIONS[user_id].append({"id": conversation_id, "title": title, "messages": []})
    return {"id": conversation_id, "title": title, "messages": []}


def get_conversations(user_id: str) -> list[dict]:
    return _CONVERSATIONS.get(user_id, [])


def add_message(user_id: str, conversation_id: str, role: str, content: str) -> dict:
    for conversation in _CONVERSATIONS.get(user_id, []):
        if conversation["id"] == conversation_id:
            message = {"role": role, "content": content}
            conversation["messages"].append(message)
            return message
    raise ValueError("Conversation not found")
