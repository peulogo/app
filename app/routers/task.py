from fastapi import APIRouter


router = APIRouter(
    prefix="/task",
    tags=["task"],
)

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

