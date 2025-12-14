# app/api/routes_categories.py
# 分类路由配置

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List

from backend.db.session import get_db
from backend.schemas.category import (
    CategoryL1Create, CategoryL1Out,
    CategoryL2Create, CategoryL2Out,
)
from backend.services import category_service

router = APIRouter(prefix="/categories", tags=["Categories"])


# ---- 一级分类 ----

# 创建一级分类
@router.post("/level1", response_model=CategoryL1Out)
def create_level1(payload: CategoryL1Create, db: Session = Depends(get_db)):
    return category_service.create_l1(db, payload)

# 获取一级分类
@router.get("/level1", response_model=List[CategoryL1Out])
def list_level1(db: Session = Depends(get_db)):
    return category_service.list_l1(db)


# ---- 二级分类 ----

# 创建二级分类
@router.post("/level2", response_model=CategoryL2Out)
def create_level2(payload: CategoryL2Create, db: Session = Depends(get_db)):
    return category_service.create_l2(db, payload)

# 获取二级分类
@router.get("/level2", response_model=List[CategoryL2Out])
def list_level2(level1_id: int | None = None, db: Session = Depends(get_db)):
    return category_service.list_l2(db, level1_id)
