# app/schemas/record.py
from datetime import datetime
from typing import List, Optional
from pydantic import BaseModel, Field, condecimal


class LedgerRecordBase(BaseModel):
    amount: condecimal(max_digits=10, decimal_places=2) = Field(..., description="金额")
    currency: str = "CNY"

    category_level1_id: Optional[int] = None
    category_level2_id: Optional[int] = None

    tags: List[str] = []

    happened_at: datetime

    note: Optional[str] = None

    is_public: bool = False
    in_bill: bool = True
    bill_id: Optional[int] = None


class LedgerRecordCreate(LedgerRecordBase):
    """创建时用的字段"""
    pass


class LedgerRecordUpdate(BaseModel):
    """更新时所有字段都可变"""
    amount: Optional[condecimal(max_digits=10, decimal_places=2)] = None
    currency: Optional[str] = None
    category_level1_id: Optional[int] = None
    category_level2_id: Optional[int] = None
    tags: Optional[List[str]] = None
    happened_at: Optional[datetime] = None
    note: Optional[str] = None
    is_public: Optional[bool] = None
    in_bill: Optional[bool] = None
    bill_id: Optional[int] = None


class LedgerRecordOut(LedgerRecordBase):
    """返回给前端的结构"""
    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True
