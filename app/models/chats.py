from dataclasses import dataclass
from dataclasses import field
from datetime import datetime


@dataclass
class ChatMessageCreate:
    content: str


@dataclass
class ChatMessage:
    id: int
    created_at: datetime
    content: str
    sender_id: int


@dataclass
class ChatCreate:
    issue_id: int


@dataclass
class Chat:
    id: int
    created_at: datetime
    issue_id: int
    messages: list[ChatMessage] = field(default_factory=list)


@dataclass
class ChatPublic:
    id: int
    created_at: datetime
    issue_id: int
    messages: list[ChatMessage] = field(default_factory=list)
