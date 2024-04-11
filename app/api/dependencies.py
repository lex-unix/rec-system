from collections.abc import Generator
from typing import Annotated

from fastapi import Depends
from fastapi import HTTPException
from redis import Redis
from sqlmodel import Session

from app.db import users
from app.db.main import engine
from app.db.models import User
from app.internal.redis import pool
from app.internal.session import Session as UserSession


def get_db() -> Generator[Session, None, None]:
    with Session(engine) as session:
        yield session


def get_redis() -> Redis:
    return Redis(connection_pool=pool)


DatabaseDep = Annotated[Session, Depends(get_db)]
RedisDep = Annotated[Session, Depends(get_redis)]
UserSessionDep = Annotated[UserSession, Depends(UserSession)]


async def authorize_user(
    db: DatabaseDep,
    user_session: UserSessionDep,
):
    session = user_session.get()

    if session is None:
        raise HTTPException(
            status_code=401, detail='You must be authorized to access resource'
        )

    try:
        user_id = int(session)
    except ValueError:
        raise HTTPException(
            status_code=401, detail='You must be authorized to access resource'
        )

    user = users.get_user_by_id(session=db, user_id=user_id)
    if not user:
        raise HTTPException(status_code=404, detail='user not found')

    return user


AuthorizeDep = Annotated[User, Depends(authorize_user)]
