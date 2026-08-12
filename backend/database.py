from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, DeclarativeBase, Mapped, mapped_column

DATABASE_URL = "sqlite:///./tm.db"


# connect_args={"check_same_thread": False}：允许跨线程使用连接
#   原因：FastAPI 处理请求是多线程的，但 SQLite 不支持多线程，必须关掉这个限制
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})


# 创建会话工厂
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


class Base(DeclarativeBase):
    id: Mapped[int] = mapped_column(primary_key=True)

