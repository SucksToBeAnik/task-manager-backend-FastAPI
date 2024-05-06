import os

from dotenv import load_dotenv
from fastapi import FastAPI, Request
import uvicorn
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

from database import Base, engine
from Routers import notes, tasks

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

templates = Jinja2Templates(directory='templates')



app.add_middleware(CORSMiddleware,allow_origins = ["*"],allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"])
app.include_router(tasks.router)
app.include_router(notes.router)


@app.get('/', response_class=HTMLResponse)
def home(request:Request):
    return templates.TemplateResponse(
        request = request, name='index.html'
    )



if __name__ == '__main__':
    os.system('uvicorn main:app --reload')

