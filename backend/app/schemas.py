
from pydantic import BaseModel, ConfigDict


class AuthorRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    name: str


class AuthorCreate(BaseModel):
    name: str


class BookCreate(BaseModel):
    title: str
    author_id: int
    price: float


class BookRead(BaseModel):
        model_config = ConfigDict(from_attributes=True)

        id: int
        title: str
        author: AuthorRead
        price: float


class Books(BaseModel):
    books: list[BookRead]


class UserCreate(BaseModel):
    email:str
    password: str

class UserRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id:int
    email:str

class Token(BaseModel):
    access_token: str
    token_type: str