from collections.abc import Generator
from typing import Annotated

from fastapi import Cookie
from fastapi import Depends
from fastapi import HTTPException
from redis import Redis
from sqlmodel import Session

from app.db import users
from app.db.main import engine
from app.internal.redis import pool
from app.internal.session import RedisStore


def get_db() -> Generator[Session, None, None]:
    with Session(engine) as session:
        yield session


def get_redis() -> Redis:
    return Redis(connection_pool=pool)


def get_session() -> RedisStore:
    return RedisStore(
        client=Redis(connection_pool=pool),
        prefix='session:',
    )


DatabaseDep = Annotated[Session, Depends(get_db)]
RedisDep = Annotated[Session, Depends(get_redis)]
UserSessionDep = Annotated[RedisStore, Depends(get_session)]


async def authorize_user(
    db: DatabaseDep,
    user_session: UserSessionDep,
    session_id: Annotated[str | None, Cookie()] = None,
):
    if session_id is None:
        raise HTTPException(
            status_code=401, detail='You must be authorized to access resource'
        )

    user_id = user_session.get_session(session_id)

    if user_id is None:
        raise HTTPException(
            status_code=401, detail='You must be authorized to access resource'
        )

    user = users.get_user_by_id(session=db, user_id=user_id)
    if not user:
        raise HTTPException(status_code=404, detail='user not found')

    return user_id


AuthorizeDep = Annotated[int, Depends(authorize_user)]
