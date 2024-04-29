import asyncpg

from app.models.feedbacks import Feedback
from app.models.feedbacks import FeedbackCreate


async def insert_feedback(
    conn: asyncpg.pool.PoolConnectionProxy,
    feedback_in: FeedbackCreate,
    issue_id: int,
):
    sql = """
        INSERT INTO feedbacks (rating, issue_id)
        VALUES ($1, $2)
        RETURNING id, created_at, updated_at
    """
    values = (feedback_in.rating, issue_id)
    row = await conn.fetchrow(sql, *values)
    feedback = Feedback(**dict(row.items()), rating=feedback_in.rating, issue_id=issue_id)  # type: ignore
    return feedback
