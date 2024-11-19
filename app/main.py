from fastapi import FastAPI
from sqlalchemy.schema import CreateTable
from app.backend.db import engine

from app.models.task import Task
from app.models.user import User
from app.routers.user import router as user_router
from app.routers.task import router as task_router

app = FastAPI()


@app.get('/')
async def read_root():
    return {"message": "Welcome to Taskmanager"}

app.include_router(task_router)
app.include_router(user_router)


print(CreateTable(User.__table__).compile(engine))
print(CreateTable(Task.__table__).compile(engine))
