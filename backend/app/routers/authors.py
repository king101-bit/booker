from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.exc import IntegrityError

from .. import models
from ..database import db_dependency
from ..schemas import AuthorCreate, AuthorRead, BookRead, Books

router = APIRouter(prefix="/authors", tags=["authors"])

def get_author_or_404(author_id: int, db: db_dependency) -> models.Author:
    author = db.get(models.Author, author_id)
    if author is None:
        raise HTTPException(status_code=404, detail="Author not found")
    return author

author_dependency = Annotated[models.Author, Depends(get_author_or_404)]

@router.get("/{author_id}/books", response_model=Books)
def get_author_books(author: author_dependency):
    return Books(books=[BookRead.model_validate(b) for b in author.books])

@router.post("", response_model=AuthorRead, status_code=201)
def create_author(author: AuthorCreate, db:db_dependency):
    db_author = models.Author(**author.model_dump())
    db.add(db_author)
    try:
        db.commit()
    except IntegrityError:
        db.rollback()
        raise HTTPException(status_code=409, detail="Author already exists")
    db.refresh(db_author)
    return db_author

@router.delete("/{author_id}", status_code=204)
def delete_author(author: author_dependency, db: db_dependency):
    if author.books:
        raise HTTPException(
            status_code=409,
            detail="Author has books, delete or reassign them first",
        )
    db.delete(author)
    db.commit()
