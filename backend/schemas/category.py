# app/schemas/category.py
from datetime import datetime
from pydantic import BaseModel
from typing import Optional, List

# -------- 一级分类 --------
class CategoryL1Base(BaseModel):
    name: str
    icon: Optional[str] = None

class CategoryL1Create(CategoryL1Base):
    pass

class CategoryL1Out(CategoryL1Base):
    id: int
    created_at: datetime

    class Config:
        orm_mode = True

# -------- 二级分类 --------
class CategoryL2Base(BaseModel):
    name: str
    level1_id: int

class CategoryL2Create(CategoryL2Base):
    pass

class CategoryL2Out(CategoryL2Base):
    id: int
    created_at: datetime

    class Config:
        orm_mode = True
