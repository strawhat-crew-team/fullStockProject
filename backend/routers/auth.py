# /routers/auth --登录注册
"""
职责: 处理 /api/register 和 /api/login HTTP请求
"""
import jwt
from fastapi import APIRouter, Depends, HTTPException, Header
from sqlalchemy.orm import Session
from database import SessionLocal, get_db
from models import User
from schemas import RegisterRequest, LoginRequest, TokenResponse
from auth import create_token, decode_token

router = APIRouter(prefix="/api", tags=["认证"])

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

@router.post("/login", response_model=TokenResponse)
def login(req: LoginRequest, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.phone == req.phone).first()
    if not user or user.password != req.password:
        raise HTTPException(status_code=401, detail="手机号或密码错误")

    token = create_token(user.id)
    return {"access_token": token, "token_type": "bearer"}


def get_current_user(authorization: str = Header(...)):
    """
    依赖函数：FastAPI收到请求后先执行本函数，校验通过才放行到接口函数
    """
    if not authorization or not authorization.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="未携带token或者格式错误")

    token = authorization.split(" ")[1]

    try:
        user_id = decode_token(token)
    except jwt.PyJWTError:
        raise HTTPException(status_code=401, detail="token已过期")

    return user_id


