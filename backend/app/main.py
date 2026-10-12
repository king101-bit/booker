from typing import Annotated

import uvicorn
from fastapi import Depends, FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, ConfigDict
from sqlalchemy.orm import Session

from . import models
from .database import SessionLocal, engine


class BookCreate(BaseModel):
    title: str
    author: str
    price: float


class BookRead(BaseModel):
        model_config = ConfigDict(from_attributes=True)

        id: int
        title: str
        author: str
        price: float


class Books(BaseModel):
    books: list[BookRead]


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

db_dependency = Annotated[Session, Depends(get_db)]

models.Base.metadata.create_all(bind=engine)

app = FastAPI()


origins = ["http://localhost:5173"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

memory_db = {"books": [], "next_id": 1}


def find_book(book_id: int) -> tuple[int, BookRead]:
    for index, book in enumerate(memory_db["books"]):
        if book.id == book_id:
            return index, book
    raise HTTPException(status_code=404, detail="Book not found")


@app.get("/books", response_model=Books)
def get_books(db: db_dependency):
   rows = db.query(models.Book).all()
   return Books(books=[BookRead.model_validate(row) for row in rows])


@app.post("/books", response_model=BookRead, status_code=201)
async def add_books(book: BookCreate, db: db_dependency):
    db_book = models.Book(**book.model_dump())
    db.add(db_book)
    db.commit()
    db.refresh(db_book)
    return db_book


@app.get("/books/{book_id}", response_model=BookRead)
def get_book(book_id: int, db: db_dependency):
    book = db.query(models.Book).filter(models.Book.id == book_id).first()
    if book is None:
        raise HTTPException(status_code=404, detail="Book not Found")
    return book


@app.delete("/books/{book_id}", status_code=204)
def delete_book(book_id: int, db: db_dependency):
    book = db.query(models.Book).filter(
        models.Book.id == book_id
    ).first()

    if book is None:
        raise HTTPException(
            status_code=404,
            detail="Book not found"
        )

    db.delete(book)
    db.commit()
    return



@app.put("/books/{book_id}", response_model=BookRead)
def update_book(book_id: int, book: BookCreate):
    index, _ = find_book(book_id)
    updated = BookRead(id=book_id, **book.model_dump())
    memory_db["books"][index] = updated
    return updated


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
