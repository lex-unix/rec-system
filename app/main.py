from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from sqlmodel import SQLModel

from app.api.main import api_router
from app.db.main import engine

SQLModel.metadata.create_all(engine)

app = FastAPI()

origins = ['http://localhost:5173']

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=['GET', 'POST', 'PUT', 'PATCH', 'DELETE'],
    allow_headers=['Accept', 'Authorization', 'Content-Type', 'X-CSRF-Token'],
)

app.include_router(api_router)
