import os

import asyncpg


async def create_db_pool():
    pool = await asyncpg.create_pool(dsn=os.environ['DATABASE_URL'])
    return pool
