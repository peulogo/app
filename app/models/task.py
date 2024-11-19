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
