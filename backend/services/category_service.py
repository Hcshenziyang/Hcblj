# app/services/category_service.py

from sqlalchemy.orm import Session
from fastapi import HTTPException

from backend.models.category import CategoryLevel1, CategoryLevel2
from backend.schemas.category import (
    CategoryL1Create, CategoryL2Create
)


# ------- 一级分类 -------
def create_l1(db: Session, data: CategoryL1Create):
    exists = db.query(CategoryLevel1).filter_by(name=data.name).first()
    if exists:
        raise HTTPException(400, "Category level1 already exists")
    c = CategoryLevel1(
        name=data.name,
        icon=data.icon,
    )
    db.add(c)
    db.commit()
    db.refresh(c)
    return c


def list_l1(db: Session):
    return db.query(CategoryLevel1).order_by(CategoryLevel1.id).all()

# ------- 二级分类 -------
def create_l2(db: Session, data: CategoryL2Create):
    parent = db.get(CategoryLevel1, data.level1_id)
    if not parent:
        raise HTTPException(404, "Level1 category not found")

    c = CategoryLevel2(
        name=data.name,
        level1_id=data.level1_id,
    )
    db.add(c)
    db.commit()
    db.refresh(c)
    return c

def list_l2(db: Session, level1_id: int = None):
    query = db.query(CategoryLevel2)
    if level1_id:
        query = query.filter_by(level1_id=level1_id)
    return query.order_by(CategoryLevel2.id).all()
