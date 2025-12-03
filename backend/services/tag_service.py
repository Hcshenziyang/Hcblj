from sqlalchemy.orm import Session
from fastapi import HTTPException
from backend.models.tag import Tag

def create_tag(db: Session, name: str):
    exists = db.query(Tag).filter_by(name=name).first()
    if exists:
        raise HTTPException(400, "Tag already exists")

    tag = Tag(name=name)
    db.add(tag)
    db.commit()
    db.refresh(tag)
    return tag


def list_tags(db: Session):
    return db.query(Tag).order_by(Tag.id).all()
