from sqlalchemy.orm import Session

from . import models, schemas


def get_user_by_name(db: Session, name: str):
    return db.query(models.User).filter(models.User.name == name).first()


def get_users(db: Session, skip: int = 0, limit: int = 100, name: str = None):
    query = db.query(models.User)

    if name:
        query = query.filter(models.User.name == name)

    return query.offset(skip).limit(limit).all()


def create_user(db: Session, user: schemas.UserCreate):
    db_user = models.User(**user.dict())
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def delete_all_users(db: Session):
    db.query(models.User).delete()
    db.commit()
