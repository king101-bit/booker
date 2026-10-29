from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException

from .. import models
from ..auth import admin_user, current_user
from ..database import db_dependency
from ..schemas import BookCreate, BookRead, Books

router = APIRouter(prefix="/books", tags=["books"])


def get_book_or_404(book_id: int, db: db_dependency) -> models.Book:
    book = db.get(models.Book, book_id)
    if book is None:
        raise HTTPException(status_code=404, detail="Book not found")
    return book


book_dependency = Annotated[models.Book, Depends(get_book_or_404)]


@router.get("", response_model=Books)
def get_books(db: db_dependency):
    rows = db.query(models.Book).all()
    return Books(books=[BookRead.model_validate(row) for row in rows])


@router.post("", response_model=BookRead, status_code=201)
def add_book(book: BookCreate, db: db_dependency, user: current_user):
    author = db.get(models.Author, book.author_id)
    if author is None:
        raise HTTPException(status_code=404, detail="Author not found")
    db_book = models.Book(**book.model_dump())
    db.add(db_book)
    db.commit()
    db.refresh(db_book)
    return db_book


@router.get("/{book_id}", response_model=BookRead)
def get_book(book: book_dependency):
    return book


@router.put("/{book_id}", response_model=BookRead)
def update_book(user: admin_user, book: book_dependency, data: BookCreate, db: db_dependency):
    author = db.get(models.Author, data.author_id)
    if author is None:
        raise HTTPException(status_code=404, detail="Author not found")

    for field, value in data.model_dump().items():
        setattr(book, field, value)
    db.commit()
    db.refresh(book)
    return book


@router.delete("/{book_id}", status_code=204)
def delete_book(user: admin_user, book: book_dependency, db: db_dependency):
    db.delete(book)
    db.commit()
