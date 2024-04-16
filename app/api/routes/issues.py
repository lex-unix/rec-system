from fastapi import APIRouter
from fastapi import HTTPException

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


@router.get('/{issue_id}')
async def get_issue(issue_id: int, db: DatabaseDep, current_user: AuthorizeDep):
    issue = issues_crud.get_issue_by_id(
        session=db,
        issue_id=issue_id,
        user_id=current_user.id,  # type: ignore
    )
    if not issue:
        raise HTTPException(status_code=404, detail='Issue not found')
    return issue
