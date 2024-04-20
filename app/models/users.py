from dataclasses import dataclass
from datetime import datetime


@dataclass
class UserBase:
    email: str
    full_name: str


@dataclass
class UserRegister:
    email: str
    full_name: str
    password: str


@dataclass
class UserLogin:
    email: str
    password: str


@dataclass
class User:
    id: int
    created_at: datetime
    updated_at: datetime
    full_name: str
    email: str
    password_hash: str


@dataclass
class UserPublic:
    id: int
    created_at: datetime
    updated_at: datetime
    email: str
    full_name: str
