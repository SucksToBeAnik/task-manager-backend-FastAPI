from fastapi import FastAPI
from Routers import tasks, notes
from database import Base, engine






description = """
## Available Routes
* **GET all tasks**
* **POST a task**
* **GET all notes**
* **POST a note**
"""

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title='Task Manager',
    description=description,
    version='0.0.1'
)

app.include_router(tasks.router)
app.include_router(notes.router)



