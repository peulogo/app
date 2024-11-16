from fastapi import APIRouter, HTTPException
from sqlalchemy import Column, Integer, String, select, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from starlette import status

from app.backend.db import Base
from sqlalchemy.orm import Session
from fastapi import Depends
from app.backend.db_depends import get_db
from app.models import User
from app.schemas import CreateUser, UpdateUser, UpdateTask, CreateTask

router = APIRouter(
    prefix="/task",
    tags=["task"],
)


class Task(Base):
    __tablename__ = 'tasks'

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    content = Column(String, nullable=False)
    priority = Column(Integer, default=0)
    completed = Column(Boolean, default=False)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False, index=True)
    slug = Column(String, unique=True, index=True)

    user = relationship("User", back_populates="tasks")


@router.get('/')
def all_tasks(db: Session = Depends(get_db)):
    tasks = db.execute(select(Task)).scalars().all()
    return tasks

@router.get('/task_id')
def task_by_id(task_id: int, db: Session = Depends(get_db)):
    task = db.execute(select(Task).filter(Task.id == task_id)).scalar()
    if task is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Task was not found")
    return task


@router.post('/create')
def create_task(create_task: CreateTask, db: Session = Depends(get_db)):
    user_id = create_task.user_id
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User was not found")

    task = Task(**create_task.dict(), user_id=user.id)

    db.add(task)
    db.commit()
    db.refresh(task)
    return {"status_code": status.HTTP_201_CREATED, "transaction": "Successful"}



@router.put("/update/{task_id}", status_code=status.HTTP_200_OK)
def update_task(task_id: int, update_task: UpdateTask, db: Session = Depends(get_db)):  # Изменили название параметра
    task = db.execute(select(Task).filter(Task.id == task_id)).scalar()
    if task is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Task was not found")

    for key, value in update_task.dict().items():
        setattr(task, key, value)

    db.commit()
    db.refresh(task)
    return {"status_code": status.HTTP_200_OK, "transaction": "Task update is successful!"}


@router.delete('/delete')
def delete_task(task_id: int, db: Session = Depends(get_db)):
    task = db.execute(select(Task).filter(Task.id == task_id)).scalar()
    if task is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Task was not found")

    db.delete(task)
    db.commit()
    return {"status_code": status.HTTP_200_OK, "transaction": "Task deletion is successful!"}


@router.get('/user_id/tasks')
def tasks_by_user_id(user_id: int, db: Session = Depends(get_db)):
    tasks = db.execute(select(Task).filter(Task.user_id == user_id)).scalars().all()  # Используем .all()
    if not tasks:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Tasks not found")
    return tasks