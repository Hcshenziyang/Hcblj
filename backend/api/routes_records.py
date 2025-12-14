# app/api/routes_records.py
# 记账基本功能路由

from typing import List
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from datetime import datetime
from backend.db.session import get_db
from backend.schemas.record import (
    LedgerRecordCreate,
    LedgerRecordUpdate,
    LedgerRecordOut,
)
from backend.services import record_service

router = APIRouter(prefix="/records", tags=["Ledger Records"])


from pydantic import BaseModel, Field, field_validator
from typing import List, Optional

# 创建记账记录
@router.post("/", response_model=LedgerRecordOut)
def create_record(payload: LedgerRecordCreate, db: Session = Depends(get_db)):
    """创建记账记录"""
    return record_service.create_record(db, payload)

# 获取记录列表
@router.get("/", response_model=List[LedgerRecordOut])
def list_records(
    start: datetime | None = None,
    end: datetime | None = None,
    category1: int | None = None,
    category2: int | None = None,
    tag: str | None = None,
    public_only: bool | None = None,
    db: Session = Depends(get_db)
):
    """获取所有记录"""
    return record_service.list_records(
        db=db,
        start=start,
        end=end,
        category1=category1,
        category2=category2,
        tag=tag,
        public_only=public_only
    )

# 获取单个记账记录
@router.get("/{record_id}", response_model=LedgerRecordOut)
def get_record(record_id: int, db: Session = Depends(get_db)):
    return record_service.get_record(db, record_id)

# 更新单个记账记录
@router.put("/{record_id}", response_model=LedgerRecordOut)
def update_record(record_id: int, payload: LedgerRecordUpdate, db: Session = Depends(get_db)):
    return record_service.update_record(db, record_id, payload)

# 删除单个记账记录
@router.delete("/{record_id}")
def delete_record(record_id: int, db: Session = Depends(get_db)):
    record_service.delete_record(db, record_id)
    return {"message": "Deleted"}

# 获取月度数据
@router.get("/monthly-report")
def monthly_report(
    year: int,
    month: int,
    db: Session = Depends(get_db)
):
    return record_service.monthly_report(db, year, month)


# 获取月度图表
@router.get("/monthly-chart")
def monthly_chart(
    year: int,
    month: int,
    db: Session = Depends(get_db)
):
    return record_service.monthly_chart(db, year, month)