from dotenv import load_dotenv
import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm import declarative_base


load_dotenv()
database_url = os.getenv("DATABASE_URL")

# database_url = "sqlite:///my-db.db"


engine = create_engine(database_url)
# engine = create_engine(database_url,connect_args={"check_same_thread":False})
create_a_session = sessionmaker(autoflush=False, autocommit=False,bind=engine)

def get_db_connection():
    db = create_a_session()
    try:
        yield db
    finally:
        db.close()
        
Base = declarative_base()