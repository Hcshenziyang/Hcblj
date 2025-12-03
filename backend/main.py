# app/main.py
from fastapi import FastAPI
from backend.api.routes_records import router as records_router
from backend.api.routes_categories import router as category_router
from backend.api.routes_tags import router as tag_router
from backend.db.session import Base, engine


# 创建数据表，开发阶段简单做法
Base.metadata.create_all(bind=engine)

app = FastAPI(title="hcblj Ledger API")

app.include_router(records_router)
app.include_router(category_router)
app.include_router(tag_router)
