from fastapi import APIRouter

from app.services.admin_service import get_admin_documents

router = APIRouter(tags=["admin"])

@router.get("/admin/documents")
async def admin_documents() -> dict:
    return {"documents": get_admin_documents()}
