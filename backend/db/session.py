# app/db/session.py
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

SQLALCHEMY_DATABASE_URL = "mysql+pymysql://root:root123@localhost:3308/hcblj?charset=utf8mb4"

# 建立连接池
engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    pool_pre_ping=True,     # 防止 MySQL 连接断开
    pool_recycle=3600,      # 3600 秒后重连，防止断开
)

# 生成session实例的设置
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

def get_db():
    from sqlalchemy.orm import Session
    db: Session = SessionLocal()
    try:
        yield db
    finally:
        db.close()
