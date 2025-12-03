from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List

from backend.db.session import get_db
from backend.schemas.tag import TagCreate, TagOut
from backend.services import tag_service

router = APIRouter(prefix="/tags", tags=["Tags"])

@router.post("/", response_model=TagOut)
def create_tag(payload: TagCreate, db: Session = Depends(get_db)):
    return tag_service.create_tag(db, payload.name)

@router.get("/", response_model=List[TagOut])
def list_tags(db: Session = Depends(get_db)):
    return tag_service.list_tags(db)
