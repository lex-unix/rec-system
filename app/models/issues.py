from datetime import datetime

from pydantic.dataclasses import dataclass

from app.models.users import Operator


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
class IssueStatusUpdate:
    status: str


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
    operator: Operator | None = None


@dataclass
class IssuePublic:
    subject: str
    type: str
    description: str
    status: str
    customer_id: int
    operator_id: int
    operator: Operator | None = None


@dataclass
class IssuesPublic:
    issues: list[IssuePublic]
