# app/models/record.py
from datetime import datetime
from sqlalchemy import (
    Column,
    Integer,
    String,
    Boolean,
    DateTime,
    Numeric,
    Text,
    ForeignKey,
)
from sqlalchemy.dialects.mysql import JSON
from backend.db.session import Base


class LedgerRecord(Base):
    __tablename__ = "hcblj_records"

    id = Column(Integer, primary_key=True, index=True)

    # 金额 10 位数字，两位小数
    amount = Column(Numeric(10, 2), nullable=False)

    # 默认货币 CNY
    currency = Column(String(3), nullable=False, default="CNY")

    # 分类
    category_level1_id = Column(Integer, ForeignKey("categories_level1.id"), nullable=True)
    category_level2_id = Column(Integer, ForeignKey("categories_level2.id"), nullable=True)

    # 标签：JSON 数组，例如 ["吃饭", "朋友"]
    tags = Column(JSON, nullable=False, default=list)

    # 发生时间
    happened_at = Column(DateTime, nullable=False, default=datetime.utcnow)

    # 备注
    note = Column(Text, nullable=True)

    # 特殊标记
    is_public = Column(Boolean, nullable=False, default=False)
    in_bill = Column(Boolean, nullable=False, default=True)

    # 关联账单（预留字段）
    bill_id = Column(Integer, nullable=True)  # 暂不要 ForeignKey

    created_at = Column(DateTime, nullable=False, default=datetime.utcnow)
    updated_at = Column(DateTime, nullable=False, default=datetime.utcnow, onupdate=datetime.utcnow)
