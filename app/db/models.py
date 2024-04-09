from sqlmodel import Field
from sqlmodel import SQLModel


class UserBase(SQLModel):
    email: str = Field(unique=True, index=True)
    full_name: str | None = None


class UserCreate(UserBase):
    password: str


class UserRegister(SQLModel):
    email: str
    password: str
    full_name: str | None = None


class UserUpdate(UserBase):
    email: str | None = None
    password: str | None = None


class User(UserBase, table=True):
    __tablename__ = 'users'
    id: int | None = Field(default=None, primary_key=True)
    password_hash: str


class UserPublic(UserBase):
    id: int
