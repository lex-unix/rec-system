from datetime import datetime
from typing import Optional

import humps

# from sqlalchemy import func
# from sqlmodel import Column
from sqlmodel import Field
from sqlmodel import Relationship
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
    created_at: datetime = Field(default_factory=datetime.utcnow)
    password_hash: str
    issues: list['Issue'] = Relationship(back_populates='user')


class UserPublic(UserBase):
    id: int


class IssueBase(CamelModel):
    subject: str
    type: str
    description: str


class IssueCreate(IssueBase):
    pass


class Issue(IssueBase, table=True):
    __tablename__ = 'issues'
    id: int | None = Field(default=None, primary_key=True)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    user_id: int | None = Field(default=None, foreign_key='users.id', nullable=False)

    user: User | None = Relationship(back_populates='issues')

    chat: Optional['Chat'] = Relationship(
        back_populates='issue', sa_relationship_kwargs={'uselist': False}
    )


class IssuePublic(IssueBase):
    id: int
    created_at: datetime
    user_id: int


class IssuesPublic(CamelModel):
    issues: list[IssuePublic]
    # count: int


class ChatBase(CamelModel):
    pass


class ChatCreate(ChatBase):
    issue_id: int


class Chat(ChatBase, table=True):
    __tablename__ = 'chats'
    id: int | None = Field(default=None, primary_key=True)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    issue_id: int | None = Field(
        default=None, foreign_key='issues.id', nullable=False, unique=True
    )

    issue: Issue | None = Relationship(back_populates='chat')

    messages: list['ChatMessage'] = Relationship(back_populates='chat')


class ChatPublic(ChatBase):
    id: int
    created_at: datetime
    issue_id: int
    messages: list['ChatMessage']


class ChatMessageBase(CamelModel):
    text: str


class ChatMessageCreate(ChatMessageBase):
    pass


class ChatMessage(ChatMessageBase, table=True):
    __tablename__ = 'chat_messages'
    id: int | None = Field(default=None, primary_key=True)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    chat_id: int | None = Field(default=None, foreign_key='chats.id', nullable=False)
    sender_id: int | None = Field(default=None, foreign_key='users.id', nullable=False)

    chat: Chat = Relationship(back_populates='messages')

    sender: User = Relationship()


class ChatMessagePublic(ChatMessageBase):
    id: int
    created_at: datetime
    chat_id: int
    sender_id: int
