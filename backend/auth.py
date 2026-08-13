# JWT签发
"""
职责：登录成功时签发token，请求进来时校验token，并取出用户
流程：登录接口验证密码 -> 签发token -> 前端保存 每次请求带上token -> 后端校验 -> 识别身份
"""


from datetime import datetime, timedelta, timezone
import jwt


# ---------- 配置（学习阶段写死，生产要挪到环境变量） ----------
SECRET_KEY = "szdjf888-szdjf666-szdjf888-szdjf666"  # 密钥
ALGORITHM = "HS256"
EXPIRE_MINUTES = 60 * 24


# 签发token
def create_token(user_id: int):
    payload = {
        "sub": str(user_id),
        "exp": datetime.now(timezone.utc) + timedelta(minutes=EXPIRE_MINUTES),
    }
    return jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)

def decode_token(token: str):
    payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
    return int(payload["sub"])



