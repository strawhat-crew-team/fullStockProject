# 统计接口
"""
职责: 处理 /api/stats/daily 和 /api/stats/efficiency 两个统计接口
"""

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import func  # func: SQLAlchemy 的函数工厂，生成SUM/COUNT等SQL聚合函数
from database import get_db
from models import Task
from routers.auth import get_current_user

router = APIRouter(prefix="/api/stats", tags=["统计"])

@router.get("/daily")
def daily_stats(user_id: int = Depends(get_current_user), db: Session = Depends(get_db)):
    """每日公式统计：按日期分组，汇总当天实际工时"""
    rows = db.query(
        Task.date,
        func.sum(Task.actual_hours).label("total_actual_hours")
    ).filter(Task.user_id == user_id, Task.date.isnot(None)).group_by(Task.date).all()
    return [{"date": str(d), "hours": round(float(h), 1)} for d, h in rows]

@router.get("/efficiency")
def efficiency(user_id: int = Depends(get_current_user), db: Session = Depends(get_db)):
    """任务完成率: 已归档任务数 / 总任务数"""
    total = db.query(func.count(Task.id)).filter(Task.user_id == user_id).scalar()
    done = db.query(func.count(Task.id)).filter(Task.user_id == user_id, Task.is_archived == True).scalar()

    rate = round(done / total, 2) if total else 0.0
    return {"total": total, "done": done, "rate": rate}


