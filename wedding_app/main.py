import pandas as pd
from typing import List
from datetime import datetime
import io
import os
import uvicorn

from fastapi import Depends, FastAPI, HTTPException, Query, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from sqlalchemy.orm import Session

from . import crud, models, schemas
from .database import SessionLocal, engine
from . import schemas

models.Base.metadata.create_all(bind=engine)

app = FastAPI()
security = HTTPBasic()

# Configure CORS
origins = [
    # Add the origin of your frontend app
    "https://suizerlyciawedding.netlify.app",
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


@app.get("/")
async def get_docs(credentials: HTTPBasicCredentials = Depends(security)):
    correct_username = os.getenv("USER")
    correct_password = os.getenv("PASSWORD")
    if not (
        credentials.username == correct_username
        and credentials.password == correct_password
    ):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Basic realm='Restricted Area'"},
        )
    return {"message": "You are authenticated"}


@app.post("/users", response_model=schemas.User)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    db_user = crud.get_user_by_name(db, name=user.name)
    if db_user:
        raise HTTPException(status_code=400, detail="User already registered")
    return crud.create_user(db=db, user=user)


@app.get("/users", response_model=List[schemas.User])
def read_users(
    key: str = Query(
        ...,
        title="Confirmation Key",
        description="Enter the confirmation key to get all users",
        min_length=1,
    ),
    skip: int = 0,
    limit: int = 100,
    name: str = None,  # Added query parameter for name
    db: Session = Depends(get_db),
):
    secret_key = os.getenv("SECRETKEY")
    if key != secret_key:
        raise HTTPException(status_code=401, detail="Invalid confirmation key")

    users = crud.get_users(db, skip=skip, limit=limit, name=name)
    return users


@app.get("/exportDB")
def export_db(
    key: str = Query(
        ...,
        title="Confirmation Key",
        description="Enter the confirmation key to download user lists",
        min_length=1,
    ),
    db: Session = Depends(get_db),
):
    secret_key = os.getenv("SECRETKEY")
    if key != secret_key:
        raise HTTPException(status_code=401, detail="Invalid confirmation key")

    users = crud.get_users(db)  # Fetch all users from the database
    if not users:
        raise HTTPException(status_code=404, detail="No users found")

    # Extract only the columns you want to export
    columns_to_export = ["id", "name", "allergic", "pax"]
    data = [{col: getattr(user, col) for col in columns_to_export} for user in users]

    # Convert data to a DataFrame
    df = pd.DataFrame(data)

    # Create a CSV file with a timestamped filename
    timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
    filename = f"guestslist_{timestamp}.csv"
    df_csv = df.to_csv(index=False)

    # Create a streaming response with the CSV content
    content = io.BytesIO(df_csv.encode())

    # Set the Content-Disposition header to force download with the specified filename
    headers = {
        "Content-Disposition": f'attachment; filename="{filename}"',
        "Content-Type": "text/csv",
    }

    return StreamingResponse(content, headers=headers)


@app.delete("/deleteDB")
def delete_db(
    key: str = Query(
        ...,
        title="Confirmation Key",
        description="Enter the confirmation key to delete all users",
        min_length=1,
    ),
    db: Session = Depends(get_db),
):
    secret_key = os.getenv("SECRETKEY")
    if key != secret_key:
        raise HTTPException(status_code=401, detail="Invalid confirmation key")

    crud.delete_all_users(db)
    return {"message": "All users deleted successfully"}


if __name__ == "__main__":
    uvicorn.run("server.api:app", host="0.0.0.0", port=8000, reload=True)
