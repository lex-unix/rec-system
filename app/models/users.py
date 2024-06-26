from datetime import datetime

from pydantic.dataclasses import dataclass


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
    is_operator: bool = False


@dataclass
class UserPublic:
    id: int
    created_at: datetime
    updated_at: datetime
    email: str
    full_name: str
    is_operator: bool


@dataclass
class Operator:
    id: int
    created_at: datetime
    updated_at: datetime
    rating: float
    availability: bool
    full_name: str
    email: str | None = None
    resolved_issues: int = 0


@dataclass
class OperatorAvailabilityUpdate:
    availability: bool
