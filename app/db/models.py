import humps
from sqlmodel import Field
from sqlmodel import SQLModel


def to_camel(string: str) -> str:
    return humps.camelize(string)


class CamelModel(SQLModel):
    class Config:
        alias_generator = to_camel
        populate_by_name = True


class UserBase(CamelModel):
    email: str = Field(unique=True, index=True)
    full_name: str | None = None


class UserCreate(UserBase):
    password: str


class UserRegister(CamelModel):
    email: str
    password: str
    full_name: str | None = None


class UserLogin(CamelModel):
    email: str
    password: str


class UserUpdate(UserBase):
    email: str | None = None  # type: ignore
    password: str | None = None


class User(UserBase, table=True):
    __tablename__ = 'users'
    id: int | None = Field(default=None, primary_key=True)
    password_hash: str


class UserPublic(UserBase):
    id: int
