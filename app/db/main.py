import os

from sqlmodel import Session, create_engine, select

from app.db.models import User, UserCreate

engine = create_engine(os.environ['DATABASE_URL'])


def init_db(session: Session) -> None:
    user = session.exec(
        select(User).where(User.email == os.environ['INIT_USER_EMAIL'])
    ).first()
    if not user:
        user_in = UserCreate(
            email=os.environ['INIT_USER_EMAIl'],
            password=os.environ[''],
        )
