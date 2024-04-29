from fastapi import APIRouter

from app.api.dependencies import AuthorizeDep
from app.api.dependencies import DBConnDep
from app.db import feedbacks as crud
from app.models.feedbacks import FeedbackCreate

router = APIRouter()


@router.post('/{issue_id}')
async def add_feedback(
    db: DBConnDep,
    current_user: AuthorizeDep,
    feedback_in: FeedbackCreate,
    issue_id: int,
):
    feedback = await crud.insert_feedback(
        conn=db,
        feedback_in=feedback_in,
        issue_id=issue_id,
    )
    return feedback
