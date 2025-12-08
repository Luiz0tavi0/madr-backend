from datetime import timedelta
from http import HTTPStatus
from typing import Annotated

import ipdb
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import delete, select
from sqlalchemy.orm import Session

from madr.core.database import get_session
from madr.core.security import (
    Token,
    authenticate_user,
    generate_token,
    get_current_user,
)
from madr.dependecies import db_session, request_form_data
from madr.models.user import User
from madr.schemas import Message
from madr.schemas.user import UserPublic, UserSchema

router = APIRouter(prefix='/users', tags=['users'])


@router.post('/token', status_code=HTTPStatus.OK, response_model=Token)
def login(form_data: request_form_data, session: db_session) -> Token:
    identity = form_data.username
    password = form_data.password
    user = authenticate_user(session, identity, password)
    if not user:
        raise HTTPException(
            status_code=HTTPStatus.UNAUTHORIZED,
            detail='Incorrect username or password',
            headers={'WWW-Authenticate': 'Bearer'},
        )
    else:
        token_delta_expire_time = timedelta(minutes=5)

        data = {'sub': user.id, 'username': user.username, 'email': user.email}

        access_token = generate_token(data, token_delta_expire_time)

        return Token(access_token=access_token, token_type='bearer')


@router.post('/', status_code=HTTPStatus.CREATED, response_model=UserPublic)
def create_user(user: UserSchema, session: Session = Depends(get_session)):
    stmt = select(User)
    stmt.where((User.username == user.username) | (User.email == user.email))
    existing_user = session.scalar(stmt)
    if existing_user:
        raise HTTPException(
            HTTPStatus.CONFLICT, detail='Conta já consta no MADR'
        )
    db_user = User(**user.model_dump())
    session.add(db_user)
    session.commit()
    session.refresh(db_user)
    return db_user


@router.put(
    '/{user_id}', status_code=HTTPStatus.CREATED, response_model=UserPublic
)
def udpate_user(
    user_id: int, user: UserSchema, session: Session = Depends(get_session)
):
    existing_user = session.scalar(select(User).where(User.id == user_id))
    if not existing_user:
        raise HTTPException(HTTPStatus.NOT_FOUND, detail='User Not Found')
    items = user.model_dump(
        exclude_unset=True, exclude={'password': True}
    ).items()
    for key, value in items:
        setattr(existing_user, key, value)
    session.commit()
    session.refresh(existing_user)
    return existing_user


# @router.get(
#     '/',
#     status_code=HTTPStatus.OK,
#     response_model=UserList,
# )
# def read_users(
#     skip: int = 0, limit: int = 10, session: Session = Depends(get_session)
# ):
#     users = session.scalars(select(User).offset(skip).limit(limit)).all()

#     return {'users': users}


@router.delete('/', status_code=HTTPStatus.OK, response_model=Message)
def remove_user(
    current_user: Annotated[UserPublic, Depends(get_current_user)],
    session: Session = Depends(get_session),
):
    try:
        # ipdb.set_trace()
        session.execute(delete(User).where(User.id == current_user.id))
        session.commit()
    except Exception:
        ipdb.set_trace()
        raise HTTPException(HTTPStatus.NOT_FOUND, 'User Not Found')
    return {'message': 'Account Removed'}
