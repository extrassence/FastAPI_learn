from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.orm import Session
from app.backend.db_depends import get_db
from typing import Annotated
from app.models import User, Task
from app.schemas import CreateTask, UpdateTask
from sqlalchemy import insert, select, update, delete
from slugify import slugify

router = APIRouter(prefix='/task', tags=['task'])


@router.get('/')
async def all_tasks(db: Annotated[Session, Depends(get_db)]):
    tasks = db.scalars(select(Task)).all()
    if not tasks:
        return HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='There are no tasks'
        )
    return tasks


@router.get('/task_id')
async def task_by_id(db: Annotated[Session, Depends(get_db)], task_id: str):
    gettask = db.scalar(select(Task).where(Task.id == task_id))
    print(gettask, task_id)
    if not gettask:
        return HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='Task was not found'
        )
    return gettask


@router.post('/create')
async def create_task(db: Annotated[Session, Depends(get_db)], createtask: CreateTask):
    check_user = db.scalar(select(User).where(User.id == createtask.user_id))
    if not check_user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f'User with id={createtask.user_id} for this task does not exist'
        )
    db.execute(insert(Task).values(title=createtask.title,
                                   priority=createtask.priority,
                                   completed=createtask.completed,
                                   user_id=createtask.user_id,
                                   slug=slugify(createtask.title)
                                   ))
    db.commit()
    return {
        'status_code': status.HTTP_201_CREATED,
        'transaction': 'Successful'
    }


@router.put('/update')
async def update_task(db: Annotated[Session, Depends(get_db)], task_id: int,
                      update_task_model: UpdateTask):
    task_update = db.scalar(select(Task).where(Task.id == task_id))
    if not task_update:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='Task was not found'
        )
    db.execute(update(Task).where(Task.id == task_id)
               .values(title=update_task_model.title,
                       priority=update_task_model.priority,
                       completed=update_task_model.completed,
                       user_id=update_task_model.user_id,
                       slug=slugify(update_task_model.title)
                       ))
    db.commit()
    return {
        'status_code': status.HTTP_200_OK,
        'transaction': 'Task update is successful!'
    }


@router.delete('/delete')
async def delete_task(db: Annotated[Session, Depends(get_db)], task_id: int):
    task_delete = db.scalar(select(Task).where(Task.id == task_id))
    if not task_delete:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='Task was not found'
        )
    db.execute(delete(Task).where(Task.id == task_id))
    db.commit()
    return {
        'status_code': status.HTTP_200_OK,
        'transaction': 'Task was deleted successfully!'
    }