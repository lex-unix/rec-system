import uuid

from redis import Redis

"""
TODO:

1. need to implement Session to conveniently set and store session (set cookie and add to redis)
2. add ttl option to RedisStore
""" ''


class RedisStore:
    def __init__(self, client: Redis, prefix: str | None = None) -> None:
        self.client = client
        self.prefix = prefix or 'sess:'
        self.ttl = 30 * 24 * 60 * 60  # 30 days

    def create_session(self, session: int):
        session_id = str(uuid.uuid4())
        key = self.prefix + session_id
        self.client.set(key, session, ex=self.ttl)
        return session_id

    def get_session(self, session_id: str):
        key = self.prefix + session_id
        return self.client.get(key)

    def destroy_session(self, session_id: str):
        key = self.prefix + session_id
        self.client.delete(key)
        pass
