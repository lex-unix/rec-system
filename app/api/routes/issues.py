from fastapi import APIRouter

from app.api.dependencies import AuthorizeDep
from app.api.dependencies import DatabaseDep
from app.db import issues as issues_crud
from app.db.models import IssueCreate

router = APIRouter()


@router.get('/')
async def list_issues(db: DatabaseDep, user: AuthorizeDep):
    issues = issues_crud.list_issues(session=db, user_id=user.id)  # type: ignore
    return issues


@router.post('/')
async def create_issue(db: DatabaseDep, user: AuthorizeDep, issue_in: IssueCreate):
    issue = issues_crud.create_issue(session=db, issue_in=issue_in, user_id=user.id)  # type: ignore
    return issue
