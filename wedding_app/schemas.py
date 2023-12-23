from pydantic import BaseModel


class UserBase(BaseModel):
    name: str
    pax: int
    allergic: str


class UserCreate(UserBase):
    pass


class User(UserBase):
    id: int

    class Config:
        orm_mode = True
