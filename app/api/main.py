from fastapi import APIRouter

from app.api.routes import issues
from app.api.routes import users

api_router = APIRouter()
api_router.include_router(users.router, prefix='/users', tags=['users'])
api_router.include_router(issues.router, prefix='/issues', tags=['issues'])
