# ============ models.py — 数据库表结构（ORM 模型） ============
# 职责：定义 User 和 Task 两张表的字段结构，对应 DEV.md 的数据库设计
# 核心思想：一个类 = 一张表，一个类属性 = 一个字段

from datetime import datetime, date as date_type  # date 改名为 date_type，避开与字段名 date 同名
from sqlalchemy import String, Boolean, Float, ForeignKey  # 字段类型和外键
from sqlalchemy.orm import Mapped, mapped_column, relationship
from database import Base  # 公共基类（database.py 定义的那层中间层）


# ---------- 用户表 ----------
class User(Base):
    __tablename__ = "users"  # 数据库里的真实表名（类名默认也能用，但显式写最稳）


    phone: Mapped[str] = mapped_column(String(20), unique=True)  # 手机号=登录账号，unique 唯一约束（重复注册会报错）
    password: Mapped[str] = mapped_column(String(100))  # 密码（学习阶段明文，生产必须哈希，DEV.md 有注明）
    nickname: Mapped[str] = mapped_column(String(50))  # 昵称
    is_admin: Mapped[bool] = mapped_column(Boolean, default=False)  # 是否管理员，默认 False（普通用户）
    created_at: Mapped[datetime] = mapped_column(default=datetime.now)  # 注册时间；插入行时自动填当前时间
    # 注意：写 datetime.now（不带括号）= 函数名，插入数据时才调用；
    #      写 datetime.now()（带括号）= 定义类时就算好了，所有行都是同一个时间，是经典错误

    # relationship：ORM 层的"关系"声明（表之间的外键是 SQL 层，这是 Python 对象层）
    # 效果：拿到 User 对象后，user.tasks 直接就是该用户的全部任务列表
    tasks: Mapped[list["Task"]] = relationship(back_populates="user")
    # "Task" 加引号 = 延迟解析（Task 类定义在下面，Python 先认识名字再说）


# ---------- 任务表 ----------
class Task(Base):
    __tablename__ = "tasks"


    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))  # 外键：指向 users 表的 id 列
    # ForeignKey("users.id") = "表名.字段名"，数据库层面保证该值必须是某个存在的用户
    code: Mapped[str] = mapped_column(String(20))  # 任务编号
    subject: Mapped[str] = mapped_column(String(100))  # 任务主题
    sub_task: Mapped[str] = mapped_column(String(200))  # 子任务描述
    target_hours: Mapped[float] = mapped_column(Float, default=0.0)  # 目标工时
    plan_hours: Mapped[float] = mapped_column(Float, default=0.0)  # 计划工时
    start_time: Mapped[datetime] = mapped_column(nullable=True)  # 开始时间；nullable=True = 允许为空（建任务时可能还没定）
    end_time: Mapped[datetime] = mapped_column(nullable=True)  # 结束时间（可空）
    actual_hours: Mapped[float] = mapped_column(Float, default=0.0)  # 实际工时
    date: Mapped[date_type] = mapped_column(nullable=True)  # 日期（可空）
    is_archived: Mapped[bool] = mapped_column(Boolean, default=False)  # 是否归档，默认未归档
    created_at: Mapped[datetime] = mapped_column(default=datetime.now)  # 创建时间

    user: Mapped["User"] = relationship(back_populates="tasks")  # 反向关系：task.user 拿到所属用户
    # relationship 两边的 back_populates 必须互相指向，成对声明
