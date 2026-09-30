from fastapi import APIRouter, HTTPException

from app.schemas.auth import TokenResponse, UserCreate, UserLogin
from app.services.auth_service import authenticate_user, register_user

router = APIRouter(tags=["auth"])

@router.post("/register", response_model=TokenResponse)
async def register(payload: UserCreate) -> TokenResponse:
    try:
        result = register_user(payload.email, payload.password, payload.full_name)
    except ValueError as exc:
        raise HTTPException(status_code=409, detail=str(exc)) from exc
    return TokenResponse(access_token=result["access_token"])

@router.post("/login", response_model=TokenResponse)
async def login(payload: UserLogin) -> TokenResponse:
    result = authenticate_user(payload.email, payload.password)
    if not result:
        raise HTTPException(status_code=401, detail="Invalid credentials")
    return TokenResponse(access_token=result["access_token"])
