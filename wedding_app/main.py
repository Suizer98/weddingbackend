import os
from typing import List
from datetime import datetime

from fastapi import Depends, FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from sqlalchemy.orm import Session

from . import crud, models, schemas
from .database import SessionLocal, engine
from . import schemas

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

# Configure CORS
origins = [
    "http://localhost:3000",  # Add the origin of your frontend app
    "https://tranquil-clafoutis-bd9fcb.netlify.app",  # Add more origins as needed
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.post("/users", response_model=schemas.User)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    db_user = crud.get_user_by_name(db, name=user.name)
    if db_user:
        raise HTTPException(status_code=400, detail="User already registered")
    return crud.create_user(db=db, user=user)


@app.get("/users", response_model=List[schemas.User])
def read_users(
    skip: int = 0,
    limit: int = 100,
    name: str = None,  # Added query parameter for name
    db: Session = Depends(get_db),
):
    users = crud.get_users(db, skip=skip, limit=limit, name=name)
    return users


@app.get("/exportDB")
def export_db():
    db_path = "wedding_app.db"  # Replace with the actual path
    if os.path.exists(db_path):
        timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
        filename = f"wedding_app_{timestamp}.db"

        return FileResponse(
            db_path, media_type="application/octet-stream", filename=filename
        )
    else:
        raise HTTPException(status_code=404, detail="Database file not found")


@app.delete("/deleteDB")
def delete_db():
    db_prefix = "wedding_app"  # Specify the prefix of the database files
    db_dir = "."  # Replace with the actual directory path

    db_files = [file for file in os.listdir(db_dir) if file.startswith(db_prefix)]

    if not db_files:
        raise HTTPException(status_code=404, detail="No matching database files found")

    for file in db_files:
        file_path = os.path.join(db_dir, file)
        os.remove(file_path)

    return {
        "message": f"All database files starting with '{db_prefix}' deleted successfully"
    }
