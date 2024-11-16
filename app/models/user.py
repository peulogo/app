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

    tasks = relationship("Task", back_populates="user")


router = APIRouter(
    prefix="/user",
    tags=["user"],
)


@router.get("/")
def all_users(db: Session = Depends(get_db)):
    users = db.execute(select(User)).scalars().all()
    return users


@router.get("/{user_id}")
def user_by_id(user_id: int, db: Session = Depends(get_db)):
    user = db.execute(select(User).filter(User.id == user_id)).scalar()
    if user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User was not found")
    return user


@router.post("/create", status_code=status.HTTP_201_CREATED)
def create_user(create_user: CreateUser, db: Session = Depends(get_db)):
    user = User(**create_user.dict())
    db.add(user)
    db.commit()
    db.refresh(user)
    return {"status_code": status.HTTP_201_CREATED, "transaction": "Successful"}


@router.put("/update/{user_id}", status_code=status.HTTP_200_OK)
def update_user(user_id: int, update_user: UpdateUser, db: Session = Depends(get_db)):
    user = db.execute(select(User).filter(User.id == user_id)).scalar()
    if user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User was not found")

    for key, value in update_user.dict().items():
        setattr(user, key, value)

    db.commit()
    db.refresh(user)
    return {"status_code": status.HTTP_200_OK, "transaction": "User update is successful!"}


@router.delete("/delete/{user_id}", status_code=status.HTTP_200_OK)
def delete_user(user_id: int, db: Session = Depends(get_db)):
    user = db.execute(select(User).filter(User.id == user_id)).scalar()
    if user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User was not found")

    db.delete(user)
    db.commit()
    return {"status_code": status.HTTP_200_OK, "transaction": "User deletion is successful!"}
