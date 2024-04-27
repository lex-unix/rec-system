#!/usr/bin/env python

import asyncio
import os

import asyncpg
import pandas as pd
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=['bcrypt'], deprecated='auto')


DATASET_PATH = os.path.join(os.getcwd(), 'datasets', 'clean_data.csv')
DEFAULT_PASSWORD = '12345678'


def form_email(name: str):
    parts = name.split(' ')
    parts = [part.lower() for part in parts]
    email = '_'.join(parts) + '@gmail.com'
    return email


def hash_password(password: str) -> str:
    return pwd_context.hash(password)


def load_data():
    data = pd.read_csv(DATASET_PATH)
    return data[:8000]


async def insert_user(conn, name, email):
    hashed_password = hash_password(DEFAULT_PASSWORD)
    return await conn.fetchval(
        """
        INSERT INTO users (full_name, email, password_hash)
        VALUES ($1, $2, $3) ON CONFLICT (email) DO NOTHING RETURNING id;
    """,
        name,
        email,
        hashed_password,
    )


async def insert_operator(conn, user_id):
    await conn.execute(
        """
        INSERT INTO operators (id, rating, availability)
        VALUES ($1, 0, TRUE) ON CONFLICT DO NOTHING;
    """,
        user_id,
    )


async def insert_issue(
    conn, subject, description, type, status, customer_id, operator_id
):
    return await conn.fetchval(
        """
        INSERT INTO issues (subject, description, type, status, customer_id, operator_id)
        VALUES ($1, $2, $3, $4, $5, $6) RETURNING id;
    """,
        subject,
        description,
        type,
        status,
        customer_id,
        operator_id,
    )


async def insert_chat(conn, issue_id):
    await conn.execute(
        """
        INSERT INTO chats (issue_id)
        VALUES ($1) ON CONFLICT DO NOTHING;
    """,
        issue_id,
    )


async def insert_feedback(conn, issue_id, rating):
    await conn.execute(
        'INSERT INTO feedbacks (rating, issue_id) VALUES ($1, $2);', rating, issue_id
    )


def snake_case(s: str):
    return '_'.join([w.lower() for w in s.split(' ')])


async def main():
    conn = await asyncpg.connect(dsn=os.environ['DATABASE_URL'])
    await conn.execute('BEGIN;')

    try:
        data = load_data()

        operator_ids = {}
        for _, item in data.iterrows():
            customer_id = await insert_user(
                conn, item['customer_name'], item['customer_email']
            )
            if customer_id is None:
                customer_id = await conn.fetchval(
                    'SELECT id FROM users WHERE email = $1;', item['customer_email']
                )

            operator_email = form_email(item['operator'])
            if operator_email not in operator_ids:
                operator_id = await insert_user(conn, item['operator'], operator_email)
                if operator_id:
                    await insert_operator(conn, operator_id)
                else:
                    operator_id = await conn.fetchval(
                        'SELECT id FROM users WHERE email = $1;', operator_email
                    )
                operator_ids[operator_email] = operator_id
            else:
                operator_id = operator_ids[operator_email]

            issue_id = await insert_issue(
                conn,
                item['ticket_subject'],
                item['ticket_description'],
                snake_case(item['ticket_type']),
                snake_case(item['ticket_status']),
                customer_id,
                operator_id,
            )
            await insert_chat(conn, issue_id)
            await insert_feedback(conn, issue_id, item['customer_satisfaction_rating'])

        await conn.execute('COMMIT;')
    except Exception as e:
        print(f'An error occurred: {e}')
        await conn.execute('ROLLBACK;')
    finally:
        await conn.close()


loop = asyncio.get_event_loop()
loop.run_until_complete(main())
