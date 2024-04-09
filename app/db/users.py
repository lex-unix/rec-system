from sqlmodel import Session
from sqlmodel import select

from app.db.models import User
from app.db.models import UserCreate
from app.internal.hash import hash_password


def create_user(session: Session, user_create: UserCreate) -> User:
    db_obj = User.model_validate(
        user_create, update={'password_hash': hash_password(user_create.password)}
    )
    session.add(db_obj)
    session.commit()
    session.refresh(db_obj)
    return db_obj


def get_user_by_email(session: Session, email: str) -> User | None:
    statement = select(User).where(User.email == email)
    user = session.exec(statement).first()
    return user
