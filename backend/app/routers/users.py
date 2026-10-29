from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from pwdlib import PasswordHash
from sqlalchemy.exc import IntegrityError

from .. import models
from ..auth import create_access_token, current_user
from ..database import db_dependency
from ..schemas import Token, UserCreate, UserRead

router = APIRouter(prefix="/users", tags=["users"])
password_hash = PasswordHash.recommended()


@router.post("", response_model=UserRead, status_code=201)
def signup(user: UserCreate, db: db_dependency):
    db_user = models.User(
        email=user.email,
        hashed_password=password_hash.hash(user.password),
    )
    db.add(db_user)
    try:
        db.commit()
    except IntegrityError:
        db.rollback()
        raise HTTPException(status_code=409, detail="Email already registered")
    db.refresh(db_user)
    return db_user

@router.post("/login", response_model=Token)
def login(form: Annotated[OAuth2PasswordRequestForm, Depends()], db:db_dependency):
    user = db.query(models.User).filter(models.User.email == form.username).first()
    if user is None or not password_hash.verify(form.password, user.hashed_password):
        raise HTTPException(status_code=401, detail="Incorrect email or password")
    return Token(access_token=create_access_token(user.email), token_type="bearer")


@router.get("/me", response_model=UserRead)
def read_me(user: current_user):
    return user
