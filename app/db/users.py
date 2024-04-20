import asyncpg

from app.models.users import User
from app.models.users import UserRegister


async def create_user(conn: asyncpg.pool.PoolConnectionProxy, user_in: UserRegister):
    sql = """
        INSERT INTO users (email, password_hash, full_name)
        VALUES ($1, $2, $3)
        RETURNING id, created_at, updated_at
    """
    values = (user_in.email, user_in.password, user_in.full_name)
    result = await conn.fetchrow(sql, *values)
    user = User(
        **dict(result),  # type: ignore
        email=user_in.email,
        full_name=user_in.full_name,
        password_hash=user_in.password,
    )
    return user


async def get_user_by_email(conn: asyncpg.pool.PoolConnectionProxy, email: str):
    sql = """
        SELECT id, created_at, updated_at, full_name, email, password_hash
        FROM users
        WHERE email = $1
    """
    row = await conn.fetchrow(sql, email)
    if row is None:
        return None
    result = User(**dict(row.items()))
    return result


async def get_user_by_id(conn: asyncpg.pool.PoolConnectionProxy, user_id: int):
    sql = """
        SELECT id, created_at, updated_at, full_name, email, password_hash
        FROM users
        WHERE id = $1
    """
    row = await conn.fetchrow(sql, user_id)
    if row is None:
        return None
    result = User(**dict(row.items()))
    return result
