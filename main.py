from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import os
from dotenv import load_dotenv
from Routers import tasks, notes
from database import Base, engine
load_dotenv()




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
    version='v0.0.1'
)


origins = os.getenv('ORIGIN_LIST')

app.add_middleware(CORSMiddleware,allow_origins = origins,allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"])
app.include_router(tasks.router)
app.include_router(notes.router)



