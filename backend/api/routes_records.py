# app/api/routes_records.py

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


@router.post("/", response_model=LedgerRecordOut)
def create_record(payload: LedgerRecordCreate, db: Session = Depends(get_db)):
    """创建记账记录"""
    return record_service.create_record(db, payload)

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

@router.get("/{record_id}", response_model=LedgerRecordOut)
def get_record(record_id: int, db: Session = Depends(get_db)):
    """获取单个记录"""
    return record_service.get_record(db, record_id)


@router.put("/{record_id}", response_model=LedgerRecordOut)
def update_record(record_id: int, payload: LedgerRecordUpdate, db: Session = Depends(get_db)):
    """更新记录"""
    return record_service.update_record(db, record_id, payload)


@router.delete("/{record_id}")
def delete_record(record_id: int, db: Session = Depends(get_db)):
    """删除记录"""
    record_service.delete_record(db, record_id)
    return {"message": "Deleted"}

@router.get("/monthly-report")
def monthly_report(
    year: int,
    month: int,
    db: Session = Depends(get_db)
):
    return record_service.monthly_report(db, year, month)

@router.get("/monthly-chart")
def monthly_chart(
    year: int,
    month: int,
    db: Session = Depends(get_db)
):
    return record_service.monthly_chart(db, year, month)