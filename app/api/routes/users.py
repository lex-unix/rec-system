from typing import Any

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
    response: Response,
) -> Any:
    user = users.get_user_by_email(session=db, email=user_in.email)

    if user:
        raise HTTPException(status_code=400, detail='user with this email already exists')

    user = users.create_user(session=db, user_create=user_in)
    session_id = user_session.create_session(user.id)  # type: ignore
    response.set_cookie(key='session_id', value=session_id, httponly=True)
    return user


@router.post('/login', response_model=UserPublic)
async def login(
    user_in: UserLogin,
    db: DatabaseDep,
    user_session: UserSessionDep,
    response: Response,
):
    user = users.get_user_by_email(session=db, email=user_in.email)
    if not user:
        raise HTTPException(status_code=404, detail='invalid authentication credentials')

    if not compare_hash(user_in.password, user.password_hash):
        raise HTTPException(status_code=401, detail='invalid authentication credentials')

    session_id = user_session.create_session(user.id)  # type: ignore
    response.set_cookie(key='session_id', value=session_id, httponly=True)
    return user


@router.get('/me', response_model=UserPublic)
async def me(user: AuthorizeDep):
    return user
