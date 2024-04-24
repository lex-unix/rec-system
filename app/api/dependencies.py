from typing import Annotated

import asyncpg
import tensorflow_recommenders as tfrs
from fastapi import Depends
from fastapi import HTTPException
from redis import Redis

from app.db.pool import create_db_pool
from app.db.users import get_user_by_id
from app.internal.redis import pool
from app.internal.session import Session as UserSession
from app.models.users import User
from nn.main import load_models

db_pool = None
ml_models = load_models()


async def get_db_pool():
    global db_pool
    if db_pool is None:
        db_pool = await create_db_pool()
    return db_pool


def get_ml_models():
    global ml_models
    if ml_models is None:
        ml_models = load_models()
    return ml_models


async def get_db_connection(pool: asyncpg.pool.Pool = Depends(get_db_pool)):
    async with pool.acquire() as connection:
        yield connection


def get_redis() -> Redis:
    return Redis(connection_pool=pool)


RedisDep = Annotated[Redis, Depends(get_redis)]
UserSessionDep = Annotated[UserSession, Depends(UserSession)]
DBConnDep = Annotated[asyncpg.pool.PoolConnectionProxy, Depends(get_db_connection)]
MLModelsDep = Annotated[dict[str, tfrs.models.Model], Depends(get_ml_models)]


async def authorize_user(
    db: DBConnDep,
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

    user = await get_user_by_id(conn=db, user_id=user_id)
    if not user:
        raise HTTPException(status_code=404, detail='user not found')

    return user


AuthorizeDep = Annotated[User, Depends(authorize_user)]
