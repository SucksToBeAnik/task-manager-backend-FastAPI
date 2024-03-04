from fastapi import APIRouter, Depends, Request, HTTPException, status
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session
from database import get_db_connection
from Models import models
from Schemas import schemas



router = APIRouter(
    prefix='/notes',
    tags=['Notes']
)




@router.get('/')
async def get_notes(db:Session = Depends(get_db_connection)):
    notes = db.query(models.Note).all()
    
    return notes



@router.post('/create')
async def create_note(request:Request, note_data: schemas.NoteSchema, db:Session=Depends(get_db_connection)):
    note_model = models.Note()
    task = db.query(models.Task).filter(models.Task.id == note_data.task_id).first()
    if task:
        note_model.task_id = note_data.task_id
        note_model.title = note_data.title
        note_model.body = note_data.body
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Invalid task id provided!')
    
    try:
        db.add(note_model)
        db.commit()
        db.refresh(note_model)
    except SQLAlchemyError as e:
        db.rollback()
        raise e
    
    return {'note':note_model,'response':'Note created successfully!'}
    