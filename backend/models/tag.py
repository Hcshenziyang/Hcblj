from sqlalchemy import Column, Integer, String, DateTime, Table, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime

from backend.db.session import Base

# 中间表：记录 <-> 标签
record_tag_association = Table(
    "record_tag_association",
    Base.metadata,
    Column("record_id", Integer, ForeignKey("hcblj_records.id")),
    Column("tag_id", Integer, ForeignKey("tags.id")),
)

class Tag(Base):
    __tablename__ = "tags"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(50), unique=True, nullable=False)

    created_at = Column(DateTime, default=datetime.utcnow)

    # 反向关联
    records = relationship(
        "LedgerRecord",
        secondary=record_tag_association,
        back_populates="tags"
    )
