from fastapi import APIRouter
from fastapi import HTTPException

import app.db.issues as crud
from app.api.dependencies import AuthorizeDep
from app.api.dependencies import DBConnDep
from app.models.issues import IssueCreate

router = APIRouter()


@router.get('/customer')
async def list_issues(db: DBConnDep, current_user: AuthorizeDep):
    issues = await crud.get_customer_issues(conn=db, customer_id=current_user.id)
    return issues


# TODO: use ml model to assign operator and create issues with assigned operator
@router.post('/')
async def create_issue(db: DBConnDep, current_user: AuthorizeDep, issue_in: IssueCreate):
    issue = await crud.create_issue(
        conn=db,
        issue_in=issue_in,
        customer_id=current_user.id,
    )
    return issue


@router.get('/customer/{issue_id}')
async def get_issue(issue_id: int, db: DBConnDep, current_user: AuthorizeDep):
    issue = await crud.get_customer_issue_by_id(
        conn=db,
        issue_id=issue_id,
        customer_id=current_user.id,
    )
    if not issue:
        raise HTTPException(status_code=404, detail='Issue not found')
    return issue
