from pydantic import BaseModel, Field, ConfigDict
from typing import Annotated
from enum import Enum
from typing import Optional



class CustomBaseModel(BaseModel):
    model_config = ConfigDict(from_attributes=True, extra='forbid')    

class StatusOption(str, Enum):
    ongoing = 'Ongoing'
    completed = 'Completed'
    will_do = 'Will Do'
        
        
class NoteSchema(CustomBaseModel):
    id:int
    task_id: int
    title: Annotated[str,Field(...,max_length=30)]
    body: Annotated[str | None,Field(max_length=500)] = 'I have nothing to say'

class UpdateNoteSchema(CustomBaseModel):
    model_config = ConfigDict(from_attributes=True, extra='forbid')

    title: Annotated[str,Field(...,max_length=30)]
    body: Annotated[str| None, Field(max_length=500)] = None

    

    


class TaskSchema(CustomBaseModel):
    title: Annotated[str,Field(max_length=30)]
    body: Annotated[str | None,Field(max_length=100)] = 'I have nothing to say'
    status: StatusOption = StatusOption.ongoing
    

class ResponseTaskSchema(TaskSchema):
    id: int
    notes: list[NoteSchema] = []
    
    

    
    
    