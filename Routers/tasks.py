from fastapi import APIRouter, Query, Request, Depends
from typing import Annotated
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