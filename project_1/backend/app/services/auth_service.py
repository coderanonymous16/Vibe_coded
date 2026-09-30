from __future__ import annotations

from sqlalchemy.orm import Session

from app.core.config import settings
from app.core.security import create_access_token, hash_password, verify_password
from app.db.database import SessionLocal
from app.db.models import User
from app.services.email_service import send_welcome_email

DEMO_EMAIL = "student@example.com"
DEMO_PASSWORD = "secret123"
DEMO_NAME = "Demo Student"


def register_user(email: str, password: str, full_name: str | None = None, db: Session | None = None) -> dict:
    normalized_email = email.strip().lower()
    session = db or SessionLocal()
    try:
        if session.query(User).filter(User.email == normalized_email).first():
            raise ValueError("User already exists")

        user = User(
            email=normalized_email,
            full_name=full_name,
            password_hash=hash_password(password),
            is_active=True,
            is_admin=False,
        )
        session.add(user)
        session.commit()
        session.refresh(user)

        result = {
            "email": user.email,
            "full_name": user.full_name,
            "access_token": create_access_token(user.email),
        }
        if settings.resend_api_key:
            try:
                import asyncio
                asyncio.run(send_welcome_email(user.email, user.full_name))
            except Exception:
                pass
        return result
    finally:
        if db is None:
            session.close()


def ensure_demo_user() -> dict:
    with SessionLocal() as session:
        user = session.query(User).filter(User.email == DEMO_EMAIL).first()
        if user is None:
            return register_user(DEMO_EMAIL, DEMO_PASSWORD, DEMO_NAME, db=session)
        return {
            "email": user.email,
            "full_name": user.full_name,
            "access_token": create_access_token(user.email),
        }


def authenticate_user(email: str, password: str, db: Session | None = None) -> dict | None:
    normalized_email = email.strip().lower()
    session = db or SessionLocal()
    try:
        user = session.query(User).filter(User.email == normalized_email).first()
        if not user:
            return None
        if not user.password_hash or not verify_password(password, user.password_hash):
            return None
        return {
            "email": user.email,
            "full_name": user.full_name,
            "access_token": create_access_token(user.email),
        }
    finally:
        if db is None:
            session.close()
