from dataclasses import asdict

from fastapi import APIRouter
from fastapi import HTTPException
from fastapi import Response

from app.api.dependencies import AuthorizeDep
from app.api.dependencies import DBConnDep
from app.api.dependencies import UserSessionDep
from app.db import users as crud
from app.internal.hash import compare_hash
from app.internal.hash import hash_password
from app.models.users import OperatorAvailabilityUpdate
from app.models.users import UserLogin
from app.models.users import UserPublic
from app.models.users import UserRegister

router = APIRouter()


@router.post('/register', response_model=UserPublic)
async def register(user_in: UserRegister, db: DBConnDep, user_session: UserSessionDep):
    user = await crud.get_user_by_email(conn=db, email=user_in.email)
    if user:
        raise HTTPException(status_code=400, detail='user with this email already exists')
    user_in.password = hash_password(user_in.password)
    user = await crud.create_user(conn=db, user_in=user_in)
    user_session.create(user.id)
    return asdict(user)


@router.post('/login', response_model=UserPublic)
async def login(user_in: UserLogin, db: DBConnDep, user_session: UserSessionDep):
    user = await crud.get_user_by_email(conn=db, email=user_in.email)
    if not user:
        raise HTTPException(status_code=404, detail='invalid authentication credentials')
    if not compare_hash(user_in.password, user.password_hash):
        raise HTTPException(status_code=401, detail='invalid authentication credentials')
    user_session.create(user.id)
    return asdict(user)


@router.post('/logout')
async def logout(user_session: UserSessionDep):
    user_session.destroy()
    return Response(status_code=200)


@router.get('/me', response_model=UserPublic)
async def me(current_user: AuthorizeDep):
    return asdict(current_user)


@router.post('/operators/{operator_id}/availability')
async def change_operator_availability(
    operator_id: int, db: DBConnDep, operator_in: OperatorAvailabilityUpdate
):
    operator = await crud.get_operator_by_id(conn=db, operator_id=operator_id)
    if not operator:
        return HTTPException(status_code=404, detail='operator not found')

    await crud.update_operator_availability(
        conn=db,
        operator_id=operator_id,
        operator_in=operator_in,
    )

    operator.availability = operator_in.availability

    return operator
