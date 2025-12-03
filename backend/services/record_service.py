# app/services/record_service.py
# 业务逻辑层
from sqlalchemy.orm import Session
from fastapi import HTTPException
from backend.models.record import LedgerRecord
from backend.schemas.record import LedgerRecordCreate,LedgerRecordUpdate
from backend.models.category import CategoryLevel1, CategoryLevel2
from datetime import datetime

def create_record(db: Session, data: LedgerRecordCreate) -> LedgerRecord:
    """创建记账记录"""
    # 验证分类存在
    if data.category_level1_id:
        if not db.get(CategoryLevel1, data.category_level1_id):
            raise HTTPException(400, "Invalid category_level1_id")
    if data.category_level2_id:
        if not db.get(CategoryLevel2, data.category_level2_id):
            raise HTTPException(400, "Invalid category_level2_id")

    new_record = LedgerRecord(
        amount=data.amount,
        currency=data.currency,
        category_level1_id=data.category_level1_id,
        category_level2_id=data.category_level2_id,
        tags=data.tags,
        happened_at=data.happened_at,
        note=data.note,
        is_public=data.is_public,
        in_bill=data.in_bill,
        bill_id=data.bill_id,
    )

    db.add(new_record)
    db.commit()
    db.refresh(new_record)
    return new_record

def list_records(db: Session, start: datetime | None = None,
                 end: datetime | None = None,
                 category1: int | None = None,
                 category2: int | None = None,
                 tag: str | None = None,
                 public_only: bool | None = None,
                 ):
    query = db.query(LedgerRecord)

    if start:
        query = query.filter(LedgerRecord.happened_at >= start)
    if end:
        query = query.filter(LedgerRecord.happened_at <= end)
    if category1:
        query = query.filter(LedgerRecord.category_level1_id == category1)
    if category2:
        query = query.filter(LedgerRecord.category_level2_id == category2)
    if tag:
        query = query.filter(LedgerRecord.tags.contains([tag]))
    if public_only is True:
        query = query.filter(LedgerRecord.is_public == True)
    return query.order_by(LedgerRecord.happened_at.desc()).all()

def get_record(db: Session, record_id: int) -> LedgerRecord:
    """获取单条记录"""
    record = db.get(LedgerRecord, record_id)
    if not record:
        raise HTTPException(status_code=404, detail="Record not found")
    return record

def update_record(db: Session, record_id: int, data: LedgerRecordUpdate) -> LedgerRecord:
    """更新记账记录"""
    # 验证分类存在
    if data.category_level1_id:
        if not db.get(CategoryLevel1, data.category_level1_id):
            raise HTTPException(400, "Invalid category_level1_id")
    if data.category_level2_id:
        if not db.get(CategoryLevel2, data.category_level2_id):
            raise HTTPException(400, "Invalid category_level2_id")

    record = db.get(LedgerRecord, record_id)
    if not record:
        raise HTTPException(status_code=404, detail="Record not found")
    update_data = data.dict(exclude_unset=True)
    for field, value in update_data.items():
        setattr(record, field, value)

    db.commit()
    db.refresh(record)
    return record

def delete_record(db: Session, record_id: int):
    """删除记录"""
    record = db.get(LedgerRecord, record_id)
    if not record:
        raise HTTPException(status_code=404, detail="Record not found")

    db.delete(record)
    db.commit()

def monthly_report(db: Session, year: int, month: int):
    # 当月范围
    start = datetime(year, month, 1)
    if month == 12:
        end = datetime(year + 1, 1, 1)
    else:
        end = datetime(year, month + 1, 1)

    query = db.query(LedgerRecord).filter(
        LedgerRecord.happened_at >= start,
        LedgerRecord.happened_at < end
    )

    records = query.all()

    # 总金额
    total = sum(r.amount for r in records)

    # 按天统计
    by_day = {}
    for r in records:
        day = r.happened_at.strftime("%Y-%m-%d")
        by_day.setdefault(day, 0)
        by_day[day] += float(r.amount)

    # 按一级分类统计
    by_cat1 = {}
    for r in records:
        if r.category_level1_id:
            cat = db.get(CategoryLevel1, r.category_level1_id).name
            by_cat1.setdefault(cat, 0)
            by_cat1[cat] += float(r.amount)

    # 按二级分类
    by_cat2 = {}
    for r in records:
        if r.category_level2_id:
            cat = db.get(CategoryLevel2, r.category_level2_id).name
            by_cat2.setdefault(cat, 0)
            by_cat2[cat] += float(r.amount)

    return {
        "month": f"{year}-{month:02d}",
        "total": float(total),
        "by_day": by_day,
        "by_category1": by_cat1,
        "by_category2": by_cat2,
    }

def monthly_chart(db: Session, year: int, month: int):
    report = monthly_report(db, year, month)

    # ① 折线图数据（每天的支出）
    line_chart = {
        "labels": list(report["by_day"].keys()),
        "values": list(report["by_day"].values())
    }

    # ② 一级分类饼图
    pie_cat1 = [
        {"name": name, "value": amount}
        for name, amount in report["by_category1"].items()
    ]

    # ③ 二级分类饼图
    pie_cat2 = [
        {"name": name, "value": amount}
        for name, amount in report["by_category2"].items()
    ]

    return {
        "month": report["month"],
        "line_chart": line_chart,
        "pie_category1": pie_cat1,
        "pie_category2": pie_cat2,
    }
