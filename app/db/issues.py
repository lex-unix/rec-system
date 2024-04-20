import asyncpg

from app.models.issues import Issue
from app.models.issues import IssueCreate


async def create_issue(
    conn: asyncpg.pool.PoolConnectionProxy,
    issue_in: IssueCreate,
    customer_id: int,
):
    sql = """
        INSERT INTO issues (subject, description, status, customer_id, operator_id)
        VALUES ($1, $2, 'in_progress', $3, 1)
        RETURNING id, created_at, updated_at
    """
    values = (issue_in.subject, issue_in.description, customer_id)
    row = await conn.fetchrow(sql, *values)
    issue = Issue(
        **dict(row.items()),  # type: ignore
        subject=issue_in.subject,
        description=issue_in.description,
        type=issue_in.type,
        customer_id=customer_id,
        operator_id=1,
        status='in_progress',
    )
    return issue


async def get_customer_issue_by_id(
    conn: asyncpg.pool.PoolConnectionProxy,
    issue_id: int,
    customer_id: int,
):
    sql = """
        SELECT i.id, i.created_at, i.updated_at, i.subject, i.description, i.status, i.type, i.customer_id, i.operator_id
        FROM issues i
        WHERE i.id = $1 AND i.customer_id = $2
    """
    values = (issue_id, customer_id)
    row = await conn.fetchrow(sql, *values)
    if not row:
        return None
    return Issue(**dict(row.items()))


# TODO: pagination
async def get_customer_issues(conn: asyncpg.pool.PoolConnectionProxy, customer_id: int):
    sql = """
        SELECT i.id, i.created_at, i.updated_at, i.subject, i.description, i.type, i.status, i.customer_id
        FROM issues i
        WHERE i.customer_id = $1
    """
    rows = await conn.fetch(sql, customer_id)
    issues = [Issue(**dict(row.items()), operator_id=1) for row in rows]
    return issues
