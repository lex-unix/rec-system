import asyncpg

from app.models.issues import Issue
from app.models.issues import IssueCreate
from app.models.issues import IssueStatusUpdate
from app.models.users import Operator


async def create_issue(
    conn: asyncpg.pool.PoolConnectionProxy,
    issue_in: IssueCreate,
    customer_id: int,
    operator_id: int,
):
    sql = """
        INSERT INTO issues (subject, description, status, type, customer_id, operator_id)
        VALUES ($1, $2, 'in_progress', $3, $4, $5)
        RETURNING id, created_at, updated_at
    """
    values = (
        issue_in.subject,
        issue_in.description,
        issue_in.type,
        customer_id,
        operator_id,
    )
    row = await conn.fetchrow(sql, *values)
    issue = Issue(
        **dict(row.items()),  # type: ignore
        subject=issue_in.subject,
        description=issue_in.description,
        type=issue_in.type,
        customer_id=customer_id,
        operator_id=operator_id,
        status='in_progress',
    )
    return issue


async def get_customer_issue_by_id(
    conn: asyncpg.pool.PoolConnectionProxy,
    issue_id: int,
    customer_id: int,
):
    sql = """
        SELECT i.id, i.created_at, i.updated_at, i.subject, i.description, i.status, i.type, i.customer_id, i.operator_id, op.rating
        FROM issues i
        JOIN operators op ON op.id = i.operator_id
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


async def get_operator_issues(conn: asyncpg.pool.PoolConnectionProxy, operator_id: int):
    sql = """
        SELECT i.id, i.created_at, i.updated_at, i.subject, i.description, i.type, i.status, i.customer_id
        FROM issues i
        WHERE i.operator_id = $1
    """
    rows = await conn.fetch(sql, operator_id)
    issues = [Issue(**dict(row.items()), operator_id=1) for row in rows]
    return issues


async def get_issue_with_operator(
    conn: asyncpg.pool.PoolConnectionProxy,
    customer_id: int,
    issue_id: int,
):
    sql = """
        SELECT i.id, i.subject, i.description, i.type, i.status, i.created_at, i.updated_at, i.customer_id,
            o.id AS operator_id, u.full_name AS operator_full_name, o.rating AS operator_rating,
            o.availability as operator_availability, u.created_at as operator_created_at, u.updated_at as operator_updated_at,
            (
                SELECT count(*)
                FROM issues
                WHERE operator_id = o.id AND status = 'closed'
            ) as resolved_issues_count,
            (
                SELECT ROUND(AVG(f.rating)::numeric, 2)
                FROM issues i2
                LEFT JOIN feedbacks f ON f.issue_id = i2.id
                WHERE
                i2.operator_id = o.id
            ) AS average_operator_rating
        FROM issues i
        LEFT JOIN operators o ON i.operator_id = o.id
        LEFT JOIN users u ON o.id = u.id
        WHERE i.id = $1
    """
    row = await conn.fetchrow(sql, issue_id)
    if not row:
        return None

    operator_data = None
    if row['operator_id'] is not None:
        operator_data = Operator(
            id=row['operator_id'],
            created_at=row['operator_created_at'],
            updated_at=row['operator_updated_at'],
            full_name=row['operator_full_name'],
            rating=row['average_operator_rating'],
            availability=row['operator_availability'],
            resolved_issues=row['resolved_issues_count'],
        )
    issue_data = {
        'id': row['id'],
        'created_at': row['created_at'],
        'updated_at': row['updated_at'],
        'subject': row['subject'],
        'description': row['description'],
        'status': row['status'],
        'type': row['type'],
        'customer_id': row['customer_id'],
        'operator_id': row['operator_id'],
        'operator': operator_data,
    }
    issue = Issue(**issue_data)
    return issue


async def delete_issue(conn: asyncpg.pool.PoolConnectionProxy, issue_id: int):
    sql = """
        DELETE FROM issues
        WHERE id = $1
    """
    result = await conn.execute(sql, issue_id)
    print(result)
    return


async def get_issue_by_id(conn: asyncpg.pool.PoolConnectionProxy, issue_id: int):
    sql = """
        SELECT i.id, i.created_at, i.updated_at, i.subject, i.description, i.type, i.status, i.customer_id, i.operator_id
        FROM issues i
        WHERE i.id = $1
    """
    row = await conn.fetchrow(sql, issue_id)
    if row is None:
        return None
    issue = Issue(**dict(row.items()))
    return issue


async def update_status(
    conn: asyncpg.pool.PoolConnectionProxy,
    issue_id: int,
    issue_in: IssueStatusUpdate,
):
    sql = """
        UPDATE issues
        SET status = $1
        WHERE id = $2
    """
    values = (issue_in.status, issue_id)
    result = await conn.execute(sql, *values)
    print(result)
