from sqlmodel import Session
from sqlmodel import col
from sqlmodel import select

from app.db.models import Issue
from app.db.models import IssueCreate


def create_issue(session: Session, issue_in: IssueCreate, user_id: int):
    db_issue = Issue.model_validate(issue_in, update={'user_id': user_id})
    session.add(db_issue)
    session.commit()
    session.refresh(db_issue)
    return db_issue


def list_issues(session: Session, user_id: int):
    statement = (
        select(Issue)
        .where(Issue.user_id == user_id)
        .order_by(col(Issue.created_at).desc())
    )
    issues = session.exec(statement).all()
    return issues
