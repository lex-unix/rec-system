from typing import Annotated

from fastapi import APIRouter
from fastapi import HTTPException
from fastapi import Query
from fastapi import WebSocket
from fastapi import WebSocketDisconnect

from app.api.dependencies import AuthorizeDep
from app.api.dependencies import DBConnDep
from app.db import chats as crud
from app.internal import ws
from app.internal.html import parse_to_html
from app.models.chats import ChatCreate
from app.models.chats import ChatMessageCreate
from nn import llama

router = APIRouter()


@router.post('/')
async def create_chat(db: DBConnDep, current_user: AuthorizeDep, chat_in: ChatCreate):
    chat = await crud.create_chat(conn=db, chat_in=chat_in)
    return chat


@router.get('/{issue_id}')
async def show_chat(
    db: DBConnDep,
    current_user: AuthorizeDep,
    issue_id: int,
):
    chat = await crud.get_chat_by_issue_id(conn=db, issue_id=issue_id)
    if chat is None:
        raise HTTPException(status_code=404, detail='chat not found')
    return chat


@router.websocket('/ws/{issue_id}')
async def chat(
    client: WebSocket,
    db: DBConnDep,
    current_user: AuthorizeDep,
    issue_id: int,
    is_chatbot: Annotated[bool, Query(alias='chat_bot')] = False,
):
    chat = await crud.get_chat_by_issue_id(conn=db, issue_id=issue_id)
    print(is_chatbot)
    if chat is None:
        raise HTTPException(status_code=404, detail='chat not found')

    await ws.manager.connect(client, room=chat.id)

    if is_chatbot:
        operator_id = await crud.get_operator_id_from_chat(conn=db, issue_id=issue_id)
        loaded_messages: list[dict] = await crud.get_last_messages(
            conn=db,
            issue_id=issue_id,
        )
        chatbot_messages = [
            {
                'role': 'user' if current_user.id == msg['sender_id'] else 'assistant',
                'content': msg['content'],
            }
            for msg in loaded_messages
        ]

    try:
        while True:
            data = await client.receive_text()
            message = {'message': data, 'userId': current_user.id}

            if not is_chatbot:
                await ws.manager.broadcast(message, sender=client, room=chat.id)

            message_in = ChatMessageCreate(content=data)
            await crud.create_message(
                conn=db,
                chat_msg_in=message_in,
                sender_id=current_user.id,  # type: ignore
                chat_id=chat.id,
            )
            if is_chatbot:
                chatbot_messages.append({'role': 'user', 'content': data})

                chatbot_reply = llama.reply(messages=chatbot_messages)
                content = parse_to_html(chatbot_reply['content'])
                chatbot_messages.append(chatbot_reply)

                message = {'message': content, 'userId': operator_id}
                await ws.manager.send_personal(message=message, client=client)

                message_in = ChatMessageCreate(content=content)
                await crud.create_message(
                    conn=db,
                    chat_msg_in=message_in,
                    sender_id=operator_id,  # type: ignore
                    chat_id=chat.id,
                )

    except WebSocketDisconnect:
        ws.manager.disconnect(client, room=chat.id)
