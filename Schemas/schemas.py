from pydantic import BaseModel, Field
from typing import Annotated
from enum import Enum


class StatusOption(str, Enum):
    ongoing = 'Ongoing'
    completed = 'Completed'
    will_do = 'Will Do'
        
        
class NoteSchema(BaseModel):
    task_id: int
    title: Annotated[str,Field(...,max_length=30)]
    body: Annotated[str | None,Field(max_length=500)] = 'I have nothing to say'
    


class TaskSchema(BaseModel):
    title: Annotated[str,Field(max_length=30)]
    body: Annotated[str | None,Field(max_length=100)] = 'I have nothing to say'
    status: StatusOption | None = 'Ongoing'
    
    
    class Config:
        form_attributes = True

class ResponseTaskSchema(TaskSchema):
    notes: list[NoteSchema] = []
    
    

    
    
    