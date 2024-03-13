from fastapi import APIRouter, Depends, Request, HTTPException, status
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session
from database import get_db_connection
from Models import models
from Schemas import schemas




# todo 1. add note delete, update and get single note functionality

router = APIRouter(
    prefix='/notes',
    tags=['Notes']
)




@router.get('/')
async def get_notes(db:Session = Depends(get_db_connection)):
    notes = db.query(models.Note).all()
    
    return notes

@router.get('/{id}')
async def get_single_note(id:int,db: Session = Depends(get_db_connection)):

    note = db.query(models.Note).get(id)

    if note is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Note with id {id} does not exist!")
    else:
        return note
    


@router.delete('/{id}')
async def delete_note(id:int,db: Session = Depends(get_db_connection)):
    note = db.query(models.Note).get(id)

    if note is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Note with id {id} does not exist!")
    else:
        try:
            db.delete(note)
            db.commit()
            return {'msg':"Note deleted!"}
        except SQLAlchemyError as e:
            raise HTTPException(status_code=status.HTTP_417_EXPECTATION_FAILED, detail='Something unexpected occurred. Please try again!')



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
    
    return {'note':note_model,'msg':'Note created successfully!'}


@router.put("/{id}")
async def update_note(id:int, note: schemas.UpdateNoteSchema, db: Session = Depends(get_db_connection)):
    note_to_update = db.query(models.Note).get(id)
    if note_to_update is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Note with id {id} does not exist!")
    else:
        try:
            note_to_update.title = note.title
            note_to_update.body = note.body
            db.commit()

            return {"msg":f"Note with id {id} updated successfully!"}
        except SQLAlchemyError as e:
            raise HTTPException(status_code=status.HTTP_417_EXPECTATION_FAILED, detail='Something unexpected occurred. Please try again!')
    