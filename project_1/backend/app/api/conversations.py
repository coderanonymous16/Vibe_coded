from __future__ import annotations

from fastapi import APIRouter, HTTPException

from app.services.conversation_service import (
    add_message,
    create_conversation,
    get_conversations,
)

router = APIRouter(tags=["conversations"])


@router.get("/conversations")
async def list_conversations(user_id: str = "demo-user") -> dict:
    return {"conversations": get_conversations(user_id)}


@router.post("/conversations")
async def create_new_conversation(title: str = "New conversation", user_id: str = "demo-user") -> dict:
    conversation = create_conversation(user_id, title)
    return conversation


@router.get("/conversations/{conversation_id}")
async def get_conversation(conversation_id: str, user_id: str = "demo-user") -> dict:
    conversations = get_conversations(user_id)
    for conversation in conversations:
        if conversation["id"] == conversation_id:
            return conversation
    raise HTTPException(status_code=404, detail="Conversation not found")


@router.patch("/conversations/{conversation_id}")
async def update_conversation(conversation_id: str, title: str, user_id: str = "demo-user") -> dict:
    conversations = get_conversations(user_id)
    for conversation in conversations:
        if conversation["id"] == conversation_id:
            conversation["title"] = title
            return conversation
    raise HTTPException(status_code=404, detail="Conversation not found")


@router.delete("/conversations/{conversation_id}")
async def delete_conversation(conversation_id: str, user_id: str = "demo-user") -> dict:
    conversations = get_conversations(user_id)
    for index, conversation in enumerate(conversations):
        if conversation["id"] == conversation_id:
            deleted = conversations.pop(index)
            return {"deleted": deleted["id"]}
    raise HTTPException(status_code=404, detail="Conversation not found")


@router.post("/conversations/{conversation_id}/messages")
async def add_conversation_message(conversation_id: str, role: str, content: str, user_id: str = "demo-user") -> dict:
    try:
        message = add_message(user_id, conversation_id, role, content)
    except ValueError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc
    return {"message": message}
