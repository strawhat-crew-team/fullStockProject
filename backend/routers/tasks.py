from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import get_db
from models import Task
from schemas import TaskCreate, TaskUpdate, TaskResponse
from routers.auth import get_current_user


# prefix: 下面所有路径自动带上 /api/tasks前缀
router = APIRouter(prefix="/api/tasks", tags=["任务"])

@router.get("", response_model=list[TaskResponse])
def list_tasks(user_id: int = Depends(get_current_user), db: Session = Depends(get_db)):
    return db.query(Task).filter(Task.user_id == user_id).all()

@router.post("", response_model=TaskResponse, status_code=201)
def create_task(req: TaskCreate, user_id: int = Depends(get_current_user), db: Session = Depends(get_db)):
    task = Task(user_id=user_id, **req.model_dump())
    db.add(task)
    db.commit()
    db.refresh(task)
    return task

@router.put("/{task_id}", response_model=TaskResponse)
def update_task(task_id: int, req: TaskUpdate, user_id: int = Depends(get_current_user), db: Session = Depends(get_db)):
    """更新任务： 只改自己的"""
    task = db.query(Task).filter(Task.id == task_id, Task.user_id == user_id).first()
    if not task:
        raise HTTPException(status_code=404, detail="任务不存在")
    for field, value in req.model_dump(exclude_unset=True).items():
        setattr(task, field, value)
    db.commit()
    db.refresh(task)
    return task

@router.delete("/{task_id}", status_code=204)
def delete_task(task_id: int, user_id: int = Depends(get_current_user), db: Session = Depends(get_db)):
    task = db.query(Task).filter(Task.id == task_id, Task.user_id == user_id).first()
    if not task:
        raise HTTPException(status_code=404, detail="任务不存在")
    db.delete(task)
    db.commit()
    # return {"message": "任务删除成功"}  # 写status_code之后不需要返回数据了

@router.post("/{task_id}/archive", response_model=TaskResponse)
def archive_task(task_id:int, user_id:int = Depends(get_current_user), db:Session = Depends(get_db)):
    task = db.query(Task).filter(Task.id == task_id, Task.user_id == user_id).first()
    if not task:
        raise HTTPException(status_code=404, detail="任务不存在")
    task.is_archived = True
    db.commit()
    db.refresh(task)
    return task

