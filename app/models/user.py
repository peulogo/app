from fastapi import APIRouter, HTTPException
from sqlalchemy import Column, Integer, String, select
from sqlalchemy.orm import relationship
from starlette import status

from app.backend.db import Base
from sqlalchemy.orm import Session
from fastapi import Depends
from app.backend.db_depends import get_db
from app.schemas import CreateUser, UpdateUser, UpdateTask


class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, nullable=False)
    firstname = Column(String, nullable=False)
    lastname = Column(String, nullable=False)
    age = Column(Integer, nullable=False)
    slug = Column(String, unique=True, index=True)

    tasks = relationship("Task", back_populates="user", cascade="all, delete")

