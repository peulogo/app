from fastapi import APIRouter

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