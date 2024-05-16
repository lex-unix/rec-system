from dataclasses import asdict

from fastapi import APIRouter
from fastapi import HTTPException
from fastapi import Response

import app.db.issues as crud
from app.api.dependencies import AuthorizeDep
from app.api.dependencies import DBConnDep
from app.api.dependencies import MLModelsDep
from app.db.users import get_operator_by_name
from app.models.issues import IssueCreate
from app.models.issues import IssueStatusUpdate
from nn.main import predict

router = APIRouter()


@router.get('/customer')
async def list_issues(db: DBConnDep, current_user: AuthorizeDep):
    issues = await crud.get_customer_issues(conn=db, customer_id=current_user.id)
    return issues


@router.post('/')
async def create_issue(
    db: DBConnDep,
    current_user: AuthorizeDep,
    issue_in: IssueCreate,
    ml_models: MLModelsDep,
):
    suggested_operators = predict(
        models=ml_models,
        customer_name=current_user.full_name,
        ticket_subject=issue_in.subject,
    )
    operator = None
    for suggestion in suggested_operators:
        operator = await get_operator_by_name(conn=db, full_name=suggestion['operator'])
        if operator:
            break
    if operator is None:
        raise HTTPException(status_code=204, detail='Could not find any operator')
    issue = await crud.create_issue(
        conn=db,
        issue_in=issue_in,
        customer_id=current_user.id,
        operator_id=operator.id,
    )
    return issue


@router.get('/customer/{issue_id}')
async def get_issue(issue_id: int, db: DBConnDep, current_user: AuthorizeDep):
    issue = await crud.get_issue_with_operator(
        conn=db,
        issue_id=issue_id,
        customer_id=current_user.id,
    )
    if not issue:
        raise HTTPException(status_code=404, detail='Issue not found')
    return asdict(issue)


@router.delete('/{issue_id}')
async def delete_issue(issue_id: int, db: DBConnDep, current_user: AuthorizeDep):
    issue = await crud.get_issue_by_id(conn=db, issue_id=issue_id)
    if issue is None:
        raise HTTPException(status_code=404, detail='issue not found')
    if issue.customer_id != current_user.id:
        raise HTTPException(status_code=403, detail="you can't delete this issue")

    await crud.delete_issue(conn=db, issue_id=issue_id)
    return Response(status_code=204)


@router.post('/customer/{issue_id}/status')
async def change_status(
    issue_id: int,
    current_user: AuthorizeDep,
    db: DBConnDep,
    issue_in: IssueStatusUpdate,
):
    issue = await crud.get_issue_with_operator(
        conn=db,
        issue_id=issue_id,
        customer_id=current_user.id,
    )
    if issue is None:
        raise HTTPException(status_code=404, detail='issue not found')
    if issue.customer_id != current_user.id:
        raise HTTPException(status_code=403, detail="you can't edit this issue")

    await crud.update_status(conn=db, issue_id=issue_id, issue_in=issue_in)

    issue.status = issue_in.status

    return issue
