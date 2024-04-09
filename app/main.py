from fastapi import FastAPI
from sqlmodel import SQLModel

from app.api.main import api_router
from app.db.main import engine

SQLModel.metadata.create_all(engine)

app = FastAPI()

app.include_router(api_router)
