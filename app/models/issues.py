from dataclasses import dataclass
from datetime import datetime


@dataclass
class IssueBase:
    subject: str
    type: str
    description: str


@dataclass
class IssueCreate:
    subject: str
    type: str
    description: str


@dataclass
class Issue:
    id: int
    created_at: datetime
    updated_at: datetime
    subject: str
    type: str
    description: str
    status: str
    customer_id: int
    operator_id: int


@dataclass
class IssuePublic:
    subject: str
    type: str
    description: str
    status: str
    customer_id: int
    operator_id: int


@dataclass
class IssuesPublic:
    issues: list[IssuePublic]
