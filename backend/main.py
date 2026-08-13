# 应用入口：创建FastAPI应用，挂载所有路由
"""
职责: 组装整个后端
"""

from contextlib import asynccontextmanager
from fastapi import FastAPI
from database import engine, Base
from routers.auth import router as auth_router
from routers.tasks  import router as tasks_router

@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    创建数据库表
    """
    Base.metadata.create_all(bind=engine)
    yield

app = FastAPI(title="tm 时间管理API", version="0.1.0", lifespan=lifespan)

@app.get("/")
async def index():
    return {"message": "后端服务已启动"}

# 把 routers/auth.py 里的 /api/register、/api/login 装进应用
app.include_router(auth_router)
app.include_router(tasks_router)


