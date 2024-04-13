from fastapi import APIRouter
from fastapi import HTTPException
from fastapi import Response

from app.api.dependencies import AuthorizeDep
from app.api.dependencies import DatabaseDep
from app.api.dependencies import UserSessionDep
from app.db import users
from app.db.models import UserCreate
from app.db.models import UserLogin
from app.db.models import UserPublic
from app.internal.hash import compare_hash

router = APIRouter()


@router.post('/register', response_model=UserPublic)
async def register(
    user_in: UserCreate,
    db: DatabaseDep,
    user_session: UserSessionDep,
):
    user = users.get_user_by_email(session=db, email=user_in.email)
    if user:
        raise HTTPException(status_code=400, detail='user with this email already exists')
    user = users.create_user(session=db, user_create=user_in)
    user_session.create(user.id)  # type: ignore
    return user


@router.post('/login', response_model=UserPublic)
async def login(user_in: UserLogin, db: DatabaseDep, user_session: UserSessionDep):
    user = users.get_user_by_email(session=db, email=user_in.email)
    if not user:
        raise HTTPException(status_code=404, detail='invalid authentication credentials')
    if not compare_hash(user_in.password, user.password_hash):
        raise HTTPException(status_code=401, detail='invalid authentication credentials')

    user_session.create(user.id)  # type: ignore
    return user


@router.post('/logout')
async def logout(user_session: UserSessionDep):
    user_session.destroy()
    return Response(status_code=200)


@router.get('/me', response_model=UserPublic)
async def me(user: AuthorizeDep):
    return user
