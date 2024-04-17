from fastapi import APIRouter
from fastapi import HTTPException
from fastapi import WebSocket
from fastapi import WebSocketDisconnect

from app.api.dependencies import AuthorizeDep
from app.api.dependencies import DatabaseDep
from app.db import chats as chat_model
from app.db.models import ChatCreate
from app.db.models import ChatMessageCreate
from app.db.models import ChatPublic
from app.internal import ws

router = APIRouter()


@router.post('/')
async def create_chat(db: DatabaseDep, current_user: AuthorizeDep, chat_in: ChatCreate):
    chat = chat_model.create_chat(session=db, chat_in=chat_in)
    return chat


@router.get('/{issue_id}', response_model=ChatPublic)
async def show_chat(
    db: DatabaseDep,
    current_user: AuthorizeDep,
    issue_id: int,
):
    chat = chat_model.get_chat_by_issue_id(session=db, issue_id=issue_id)
    if chat is None:
        raise HTTPException(status_code=404, detail='chat not found')
    return chat


@router.websocket('/ws/{issue_id}')
async def chat(
    client: WebSocket,
    db: DatabaseDep,
    current_user: AuthorizeDep,
    issue_id: int,
):
    chat = chat_model.get_chat_by_issue_id(session=db, issue_id=issue_id)
    if chat is None:
        raise HTTPException(status_code=404, detail='chat not found')

    await ws.manager.connect(client, room=chat.id)
    try:
        while True:
            data = await client.receive_text()
            message = {'message': data, 'userId': current_user.id}
            await ws.manager.broadcast(message, sender=client, room=chat.id)
            message_in = ChatMessageCreate(text=data)
            chat_model.create_message(
                session=db,
                chat_msg_in=message_in,
                sender_id=current_user.id,  # type: ignore
                chat_id=chat.id,
            )

    except WebSocketDisconnect:
        ws.manager.disconnect(client, room=chat.id)
