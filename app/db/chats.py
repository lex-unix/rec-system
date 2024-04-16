from sqlmodel import Session
from sqlmodel import col
from sqlmodel import select

from app.db.models import Chat
from app.db.models import ChatCreate
from app.db.models import ChatMessage
from app.db.models import ChatMessageCreate


def create_chat(session: Session, chat_in: ChatCreate):
    db_obj = Chat.model_validate(chat_in)
    session.add(db_obj)
    session.commit()
    session.refresh(db_obj)
    return db_obj


def get_chat_by_issue_id(session: Session, issue_id: int):
    statement = (
        select(Chat)
        .where(Chat.issue_id == issue_id)
        .outerjoin(ChatMessage, Chat.issue_id == ChatMessage.chat_id)  # type: ignore
        .order_by(col(ChatMessage.created_at).desc())
    )
    chat = session.exec(statement).first()
    return chat


def create_message(
    session: Session,
    chat_msg_in: ChatMessageCreate,
    sender_id: int,
    chat_id: int,
):
    db_obj = ChatMessage.model_validate(
        chat_msg_in,
        update={'sender_id': sender_id, 'chat_id': chat_id},
    )
    session.add(db_obj)
    session.commit()
    session.refresh(db_obj)
    return db_obj
