import uuid
from abc import ABC
from abc import abstractmethod
from typing import Annotated

from fastapi import Cookie
from fastapi import Response
from redis import Redis

from app.internal.redis import pool

"""
TODO:

1. need to implement Session to conveniently set and store session (set cookie and add to redis)
2. add ttl option to RedisStore
""" ''

SESSION_MAX_AGE = 30 * 24 * 60 * 60  # 30 days


class Store(ABC):
    @abstractmethod
    def set(self, session_id: str, session: int) -> str:
        pass

    @abstractmethod
    def get(self, session_id: str):
        pass

    @abstractmethod
    def destroy(self, session_id: str):
        pass


class RedisStore(Store):
    def __init__(self, client: Redis, prefix: str | None = None) -> None:
        self.client = client
        self.prefix = prefix or 'sess:'
        self.ttl = SESSION_MAX_AGE

    def set(self, session_id: str, session: int) -> str:
        key = self.prefix + session_id
        self.client.set(key, session, ex=self.ttl)
        return session_id

    def get(self, session_id: str):
        key = self.prefix + session_id
        val = self.client.get(key)
        return val

    def destroy(self, session_id: str):
        key = self.prefix + session_id
        self.client.delete(key)


# i should figure how to create redis client
# i don't know shit about python redis
redis = Redis(connection_pool=pool)
store = RedisStore(client=redis, prefix='user_session:')


class Session:
    store = store
    cookie_name = 'session_id'
    cookie_max_age = SESSION_MAX_AGE
    cookie_same_site = 'lax'
    cookie_secure = False
    cookie_http_only = True

    def __init__(
        self,
        response: Response,
        session_id: Annotated[str | None, Cookie()] = None,
    ):
        self.response = response
        self.session_id = session_id

    def create(self, data: int) -> None:
        """
        Creates a new session by setting a cookie and saving data to the store.

        Args:
            data (int): The data to be saved in the store (e.g., a user ID).

        This method generates a new session ID using UUID4, saves the provided data
        in the store with the generated session ID as the key, and sets a cookie
        with the session ID. The cookie is configured with various options such as
        max_age, samesite, secure, and httponly based on the respective class attributes.
        """
        if self.session_id:
            session_id = self.session_id
        else:
            session_id = str(uuid.uuid4())

        self.store.set(session_id, data)

        self.response.set_cookie(
            key=self.cookie_name,
            value=session_id,
            max_age=self.cookie_max_age,
            samesite=self.cookie_same_site,
            secure=self.cookie_secure,
            httponly=self.cookie_http_only,
        )

    def get(self) -> str | None:
        """
        Retrieves the session data from the store if it exists, otherwise returns None.

        Returns:
            str | None: The session data if the session exists, or None if no session is found.
        """
        if self.session_id is None:
            return None

        session = self.store.get(self.session_id)
        return session

    def destroy(self) -> None:
        """
        Destroys the current session if it exists.

        This method deletes the session from the store and sets the cookie
        value to an empty string with an expiration time of 0 (expired).
        If no session exists (self.session_id is None), it returns without any action.
        """
        if self.session_id is None:
            return
        self.store.destroy(self.session_id)
        self.response.set_cookie(self.cookie_name, value='', max_age=0)
