from fastapi import APIRouter
from sqlalchemy import Column, Integer, String, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from app.backend.db import Base

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
async def all_tasks():
    return


@router.get('/task_id')
async def task_by_id():
    return


@router.post('/create')
async def create_task():
    return


@router.put('/update')
async def update_task():
    return


@router.delete('/delete')
async def delete_task():
    return
