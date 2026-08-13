# /routers/auth --登录注册
"""
职责: 处理 /api/register 和 /api/login HTTP请求
"""

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import SessionLocal
from models import User
from schemas import RegisterRequest, LoginRequest, TokenResponse
from auth import create_token

router = APIRouter(prefix="/api", tags=["认证"])


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/register")
def register(req: RegisterRequest, db: Session = Depends(get_db)):
    exists = db.query(User).filter(User.phone == req.phone).first()
    if exists:
        raise HTTPException(status_code=400, detail="手机号已存在")

    # 构造User对象
    user = User(phone=req.phone, password=req.password, nickname=req.nickname)
    db.add(user)
    db.commit()
    db.refresh(user)

    return {"message": "注册成功"}

@router.post("/login")
def login(req: LoginRequest, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.phone == req.phone).first()
    if not user or user.password != req.password:
        raise HTTPException(status_code=401, detail="手机号或密码错误")

    token = create_token(user.id)
    return {"access_token": token, "token_type": "bearer"}


