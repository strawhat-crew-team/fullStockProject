# ============ schemas.py — 请求/响应模型（Pydantic） ============
from datetime import datetime, date as date_type
from pydantic import BaseModel, ConfigDict

class RegisterRequest(BaseModel):
    """注册接口参数"""
    phone: str
    password: str
    nickname: str

class LoginRequest(BaseModel):
    """登录请求体：POST /api/login 收什么"""
    phone: str  # 手机号
    password: str  # 密码


class TokenResponse(BaseModel):
    """登录成功响应：POST /api/login 回什么"""
    access_token: str  # JWT 字符串
    token_type: str  # 固定 "bearer"


# ---------- 任务模块 ----------
class TaskCreate(BaseModel):
    """创建任务请求体：POST /api/tasks 收什么
    对应 task 表除 id / user_id / created_at 外的字段（这三个是数据库自己管的）"""
    code: str  # 任务编号
    subject: str  # 任务主题
    sub_task: str  # 子任务描述
    target_hours: float = 0.0  # 目标工时；写了默认值 = 前端不传也合法（可选参数）
    plan_hours: float = 0.0  # 计划工时
    start_time: datetime | None = None  # 开始时间；| None 联合类型 = 可空
    end_time: datetime | None = None  # 结束时间（可空）
    actual_hours: float = 0.0  # 实际工时
    date: date_type | None = None  # 日期（可空）——date_type 别名，models.py 同款教训
    is_archived: bool = False  # 是否归档，默认 False


class TaskUpdate(BaseModel):
    """更新任务请求体：PUT /api/tasks/{id} 收什么
    与 TaskCreate 的差别：所有字段默认 None——只传要改的字段，不传的保持原样"""
    code: str | None = None
    subject: str | None = None
    sub_task: str | None = None
    target_hours: float | None = None
    plan_hours: float | None = None
    start_time: datetime | None = None
    end_time: datetime | None = None
    actual_hours: float | None = None
    date: date_type | None = None
    is_archived: bool | None = None


class TaskResponse(BaseModel):
    """任务响应：创建/更新/列表/详情接口统一用它回数据"""
    model_config = ConfigDict(from_attributes=True)
    # from_attributes=True：允许"直接从 ORM 对象转成这个模型"
    # 效果：拿到 SQLAlchemy 的 task 对象后，TaskResponse.model_validate(task)
    # 一步转换，不用手动逐个字段搬——后面 routers 里会用到

    id: int  # 任务 id（数据库自增）
    user_id: int  # 归属用户 id
    code: str  # 任务编号
    subject: str  # 任务主题
    sub_task: str  # 子任务描述
    target_hours: float  # 目标工时
    plan_hours: float  # 计划工时
    start_time: datetime | None = None  # 开始时间
    end_time: datetime | None = None  # 结束时间
    actual_hours: float  # 实际工时
    date: date_type | None = None  # 日期
    is_archived: bool  # 是否归档
    created_at: datetime  # 创建时间

