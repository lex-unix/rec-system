import json

import asyncpg

from app.models.chats import Chat
from app.models.chats import ChatCreate
from app.models.chats import ChatMessage
from app.models.chats import ChatMessageCreate


async def create_chat(conn: asyncpg.pool.PoolConnectionProxy, chat_in: ChatCreate):
    sql = """
        INSERT INTO chats (issue_id)
        VALUES ($1)
        RETURNING id, created_at
    """
    row = await conn.fetchrow(sql, chat_in.issue_id)
    chat = Chat(**dict(row.items()), issue_id=chat_in.issue_id)  # type: ignore
    return chat


async def get_chat_by_issue_id(conn: asyncpg.pool.PoolConnectionProxy, issue_id: int):
    sql = """
        SELECT
            c.id,
            c.issue_id,
            c.created_at,
            (
                SELECT
                    COALESCE(json_agg(
                        json_build_object(
                            'id', m.id,
                            'content', m.content,
                            'created_at', m.created_at,
                            'sender_id', m.sender_id
                        )
                        ORDER BY m.created_at, m.id ASC
                    ), '[]')
                FROM chat_messages m
                WHERE m.chat_id = c.id
            ) as messages
        FROM chats c
        WHERE c.issue_id = $1
    """
    row = await conn.fetchrow(sql, issue_id)
    if not row:
        return None

    messages_data = json.loads(row['messages'])
    chat_data = {
        'id': row['id'],
        'created_at': row['created_at'],
        'issue_id': row['issue_id'],
        'messages': [ChatMessage(**message_data) for message_data in messages_data],
    }
    chat = Chat(**chat_data)
    return chat


async def create_message(
    conn: asyncpg.pool.PoolConnectionProxy,
    chat_msg_in: ChatMessageCreate,
    sender_id: int,
    chat_id: int,
):
    sql = """
        INSERT INTO chat_messages (chat_id, sender_id, content)
        VALUES ($1, $2, $3)
        RETURNING id, created_at
    """

    values = (chat_id, sender_id, chat_msg_in.content)
    row = await conn.fetchrow(sql, *values)
    chat_msg = ChatMessage(
        **dict(row.items()),  # type: ignore
        sender_id=sender_id,
        content=chat_msg_in.content,
    )
    return chat_msg


# use only when chatbot flag is set to True
async def get_operator_id_from_chat(
    conn: asyncpg.pool.PoolConnectionProxy,
    issue_id: int,
):
    sql = """
        SELECT issues.operator_id
        FROM issues
        WHERE issues.id = $1;
    """
    operator_id = await conn.fetchval(sql, issue_id)

    return operator_id


# only used to load previous chat messages for a chatbot
async def get_last_messages(
    conn: asyncpg.pool.PoolConnectionProxy,
    issue_id: int,
    limit=10,
):
    sql = """
        SELECT chat_messages.sender_id, chat_messages.content
        FROM chat_messages
        INNER JOIN chats ON chat_messages.chat_id = chats.id
        WHERE chats.issue_id = $1
        ORDER BY chat_messages.created_at DESC
        LIMIT $2;
    """
    values = (issue_id, limit)
    rows = await conn.fetch(sql, *values)
    return rows
