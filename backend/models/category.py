# app/models/category.py
from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime
from backend.db.session import Base


class CategoryLevel1(Base):
    __tablename__ = "categories_level1"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(50), nullable=False, unique=True)
    icon = Column(String(50), nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    level2 = relationship("CategoryLevel2", back_populates="level1")


class CategoryLevel2(Base):
    __tablename__ = "categories_level2"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(50), nullable=False)
    level1_id = Column(Integer, ForeignKey("categories_level1.id"), nullable=False)
    level1 = relationship("CategoryLevel1", back_populates="level2")
    created_at = Column(DateTime, default=datetime.utcnow)
