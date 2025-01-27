from fastapi import APIRouter, Depends, status, HTTPException
# Сессия БД
from sqlalchemy.orm import Session
# Функция подключения к БД
from app.backend.db_depends import get_db
# Аннотации, Модели БД и Pydantic.
from typing import Annotated
from app.models import *
from app.schemas import *
# Функции работы с записями.
from sqlalchemy import insert, select, update, delete
# Функция создания slug-строки
from slugify import slugify

router = APIRouter(prefix='/user', tags=['user'])


@router.get('/')
async def all_users(db: Annotated[Session, Depends(get_db)]):
    users = db.scalars(select(User)).all()
    if users is None:
        return HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='There are no users.'
        )
    return users


@router.get('/user_id')
async def user_by_id(db: Annotated[Session, Depends(get_db)], user_id: str):
    getuser = db.scalars(select(User).where(User.id == user_id))
    if getuser is None:
        return HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='User not found.'
        )
    return getuser


@router.post('/create')
async def create_user(db: Annotated[Session, Depends(get_db)], createuser: CreateUser):
    db.execute(insert(User).values(username=createuser.username,
                                   firstname=createuser.firstname,
                                   lastname=createuser.lastname,
                                   age=createuser.age,
                                   slug=slugify(createuser.username)
                                   ))
    db.commit()
    return {
        'status_code': status.HTTP_201_CREATED,
        'transaction': 'User has been created.'
    }


@router.put('/update')
async def update_user(db: Annotated[Session, Depends(get_db)], user_id: int,
                      update_user_model: UpdateUser):
    user_update = db.scalar(select(User).where(User.id == user_id))
    if user_update is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='User not found.'
        )
    db.execute(update(User).where(User.id == user_id)
               .values(firstname=update_user_model.firstname,
                       lastname=update_user_model.lastname,
                       age=update_user_model.age
                       # slug=slugify(update_user_model.lastname)
                       ))
    db.commit()
    return {
        'status_code': status.HTTP_200_OK,
        'transaction': 'User has been updated.'
    }


@router.delete('/delete')
async def delete_user(db: Annotated[Session, Depends(get_db)], user_id: int):
    user_update = db.scalar(select(User).where(User.id == user_id))
    if user_update is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='User not found.'
        )

    db.execute(delete(User).where(User.id == user_id))
    db.commit()
    return {
        'status_code': status.HTTP_200_OK,
        'transaction': 'User has been deleted.'
    }
