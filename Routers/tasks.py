from typing import Annotated

from fastapi import APIRouter, Depends, Query, Request, status
from fastapi.exceptions import HTTPException
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session

from database import get_db_connection
from Models import models
from Schemas import schemas

router = APIRouter(prefix='/tasks',tags=['Tasks'])


description = """
# Fetches tasks
"""
@router.get('/',description=description, response_model=list[schemas.ResponseTaskSchema])
async def get_tasks(db:Session = Depends(get_db_connection)):
    tasks = db.query(models.Task).all()
    return tasks

@router.get('/{id}', status_code=status.HTTP_302_FOUND)
async def get_single_task(id:int,db: Session = Depends(get_db_connection)):
    try:
        task = db.query(models.Task).get(id)
        if task is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Task with id {id} does not exist!")
        else:
            return task
    except SQLAlchemyError:
        raise HTTPException(status_code=status.HTTP_417_EXPECTATION_FAILED, detail='Something unexpected occurred. Please try again!')

@router.post('/create')
async def create_a_task(request: Request, task_data: schemas.TaskSchema, db:Session = Depends(get_db_connection)):
    task_model = models.Task()

    task_model.title = task_data.title
    task_model.body = task_data.body
    task_model.status = task_data.status
    
    try:
        db.add(task_model)
        db.commit()
        db.refresh(task_model)
    except SQLAlchemyError as e:
        db.rollback()
        raise e
    
    return {'task':task_model, 'response':"Task created successfully!"}


@router.put('/{id}',status_code=status.HTTP_200_OK)
async def update_task(id:int,task: schemas.TaskSchema, db: Session = Depends(get_db_connection)):
    task_to_update = db.query(models.Task).get(id)

    if task_to_update is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Task with id {id} does not exist!")
    else:
        task_to_update.title = task.title
        task_to_update.body = task.body
        task_to_update.status = task.status

        db.commit()

        return {'msg':'Task updated successfully!'}




@router.delete('/{id}')
async def delete_task(id: int,db: Session = Depends(get_db_connection)):
    task_to_delete = db.query(models.Task).get(id)

    if task_to_delete is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Task with id {id} does not exist!")
    else:
        db.delete(task_to_delete)
        db.commit()
        return {'msg':f"Successfully deleted task with id {id}!"}

