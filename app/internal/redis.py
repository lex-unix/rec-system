import os

import redis


def create_redis():
    print('redis create function')
    return redis.ConnectionPool(
        host=os.environ['REDIS_HOST'],
        port=os.environ['REDIS_PORT'],
        db=0,
        decode_responses=True,
    )


pool = create_redis()
