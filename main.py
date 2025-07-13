# pylint: disable=no-name-in-module
# pylint: disable=no-self-argument
# pylint: disable=missing-function-docstring
# pylint: disable=missing-class-docstring
# pylint: disable=line-too-long

# Modules
import requests
from fastapi import FastAPI, HTTPException, status, Depends
from sqlalchemy import create_engine, Column, Integer, String, DateTime, func
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy.ext.declarative import declarative_base
from pydantic import BaseModel
from datetime import datetime
from typing import List

# Test for frontend
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse

# Initialize database  
SQLALCHEMY_DATABASE_URL = "sqlite:///./animals.db"
engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# Manage database sessions 
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Define data types 
class Picture(Base):
    __tablename__ = "pictures"
    id = Column(Integer, primary_key=True)
    animal_type = Column(String, index=True)
    url = Column(String)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

class PictureResponse(BaseModel):
    id: int
    animal_type: str
    url: str
    created_at: datetime

    class Config:
        orm_mode = True

# Create database table
Base.metadata.create_all(bind=engine)

# FastAPI 
app = FastAPI(title="Animal Picture App")

# Test for frontend 
app.mount("/static", StaticFiles(directory="static"), name="static")

ANIMAL_APIS = {
    #"cat": "https://placekitten.com/200/300",  # offline
    #"duck":"https://random-d.uk/api/GET/random",
    "fox": "https://randomfox.ca/floof/",
    "dog": "https://place.dog/300/200",
    "bear": "https://placebear.com/200/300",
}

# Test for frontend 
@app.get("/", response_class=FileResponse)
def read_root():
    return "static/index.html"

# Endpoints 
# POST, to fetch a new picture 
@app.post("/pictures/fetch/", response_model=List[PictureResponse], status_code=status.HTTP_201_CREATED)
def fetch_and_save_pictures(animal_type: str, num_pictures: int, db: Session = Depends(get_db)):
    """
    Gets and saves pictures.
    """
    animal_type = animal_type.lower()

    # only use availabe animals 
    if animal_type not in ANIMAL_APIS:
        raise HTTPException(status_code=400, detail="Invalid animal.")

    # fetch at least one picture, not more than ten at once 
    if not (1 <= num_pictures <= 10):
        raise HTTPException(status_code=400, detail="Number of pictures must be between 1 and 10.")

    saved_pictures = []
    api_url = ANIMAL_APIS[animal_type]

    for i in range(num_pictures):

        final_url = ""
        request_url = api_url

        if animal_type in ['dog', 'bear']:
            request_url = f"{api_url}?cachebust={i}" # avoid fetichng the same cached picture 
        
        try:
            response = requests.get(request_url)
            response.raise_for_status()

            if animal_type == 'fox':
                final_url = response.json()['image'] # get 'image' from JSON-response
            else:
                final_url = response.url # URL from dog/bear 

            db_picture = Picture(animal_type=animal_type, url=final_url)
            db.add(db_picture)
            db.commit()
            db.refresh(db_picture)
            saved_pictures.append(db_picture)
            
        except requests.exceptions.RequestException as error:
            db.rollback() # if one request fails
            raise HTTPException(status_code=503, detail=f"External API error: {error}")

    return saved_pictures

# GET, to show the latest picture  
@app.get("/pictures/last/", response_model=PictureResponse)
def get_last_picture(animal_type: str, db: Session = Depends(get_db)):
    """
    Gets the latest picture.
    """
    last_picture = db.query(Picture)\
        .filter(Picture.animal_type == animal_type.lower())\
        .order_by(Picture.id.desc())\
        .first()

    if not last_picture:
        raise HTTPException(status_code=404, detail="No pictures found.")

    return last_picture