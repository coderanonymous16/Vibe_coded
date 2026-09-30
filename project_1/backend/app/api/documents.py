from __future__ import annotations

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.db.database import get_db
from app.services.document_service import get_documents, get_subjects

router = APIRouter(tags=["documents"])


@router.get("/documents")
async def list_documents(db: Session = Depends(get_db)) -> dict:
    return {"documents": get_documents(db)}


@router.get("/subjects")
async def list_subjects(db: Session = Depends(get_db)) -> dict:
    return {"subjects": get_subjects(db)}
