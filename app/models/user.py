from fastapi import APIRouter
from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from app.backend.db import Base

class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, nullable=False)
    firstname = Column(String, nullable=False)
    lastname = Column(String, nullable=False)
    age = Column(Integer, nullable=False)
    slug = Column(String, unique=True, index=True)

    tasks = relationship("Task", back_populates="user")


router = APIRouter(
    prefix="/user",
    tags=["user"],
)



@router.get('/')
async def all_users():
    return


@router.get('/user_id')
async def user_by_id():
    return


@router.post('/create')
async def create_user():
    return


@router.put('/update')
async def update_user():
    return


@router.delete('/delete')
async def delete_user():
    return

