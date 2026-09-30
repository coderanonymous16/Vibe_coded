from __future__ import annotations

import httpx

from app.core.config import settings


async def send_welcome_email(email: str, full_name: str | None = None) -> bool:
    if not settings.resend_api_key or not settings.resend_from_email:
        return False

    payload = {
        "from": settings.resend_from_email,
        "to": [email],
        "subject": "Welcome to ExamRAG",
        "html": (
            "<p>Hello "
            + (full_name or "student")
            + ",</p><p>Welcome to ExamRAG. Your account is ready and you can start asking academic questions immediately.</p>"
        ),
    }

    try:
        response = httpx.post(
            "https://api.resend.com/emails",
            headers={
                "Authorization": f"Bearer {settings.resend_api_key}",
                "Content-Type": "application/json",
            },
            json=payload,
            timeout=20.0,
        )
        return response.is_success
    except Exception:
        return False
