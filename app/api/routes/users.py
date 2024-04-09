from typing import Any

from fastapi import APIRouter, HTTPException, Response

from app.api.dependencies import DatabaseDep, UserSessionDep
from app.db import users
from app.db.models import UserCreate, UserPublic

router = APIRouter()


@router.post('/', response_model=UserPublic)
async def create_user(
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
