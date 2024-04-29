from datetime import datetime

from pydantic.dataclasses import dataclass


@dataclass
class FeedbackBase:
    rating: float


@dataclass
class FeedbackCreate:
    rating: float


@dataclass
class Feedback:
    id: int
    created_at: datetime
    updated_at: datetime
    rating: float
    issue_id: int
