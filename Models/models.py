from database import Base
from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship, mapped_column, Mapped
from typing import List, Optional


class Task(Base):
    __tablename__ = 'task'
    
    id : Mapped[int] = mapped_column(nullable=False, index=True, primary_key=True,unique=True, autoincrement='auto')
    title : Mapped[str] = mapped_column( nullable=False)
    body: Mapped[Optional[str]] = mapped_column(nullable=True)
    status: Mapped[Optional[str]] 
    
    notes: Mapped[Optional[List['Note']]] = relationship(back_populates='task',cascade="all, delete-orphan")
    
    
class Note(Base):
    __tablename__ = 'note'
    
    id : Mapped[int] = mapped_column(nullable=False, index=True, primary_key=True, autoincrement='auto',unique=True)
    task_id : Mapped[int] = mapped_column(ForeignKey(column='task.id'))
    
    title : Mapped[str] = mapped_column(nullable=False)
    body: Mapped[Optional[str]] = mapped_column(nullable=True)
    
    task: Mapped['Task'] = relationship(back_populates='notes')
    
    