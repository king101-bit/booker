from datetime import datetime, timedelta, timezone
from typing import Annotated

import jwt
from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from jwt import InvalidTokenError

from . import models
from .config import settings
from .database import db_dependency

ALGORITHIM = "HS256"
TOKEN_MINUTES = 30

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="users/login")

def get_current_user(token: Annotated[str, Depends(oauth2_scheme)], db:db_dependency) -> models.User:
    try:
        payload = jwt.decode(token, settings.secret_key, algorithms=[ALGORITHIM])
        email = payload.get("sub")
    except InvalidTokenError:
        raise HTTPException(status_code=401, detail="Invalid or expired token")
    user = db.query(models.User).filter(models.User.email == email).first()
    if user is None:
        raise HTTPException(status_code=401, detail="Invalid or expired token")
    return user

current_user = Annotated[models.User, Depends(get_current_user)]

def require_admin(user: current_user) -> models.User:
    if user.role != "admin":
        raise HTTPException(status_code=403, detail="Admin access required")
    return user

admin_user = Annotated[models.User, Depends(require_admin)]

def create_access_token(email:str) -> str:
    expire = datetime.now(timezone.utc) + timedelta(minutes=TOKEN_MINUTES)
    return jwt.encode({"sub": email, "exp": expire}, settings.secret_key, algorithm=ALGORITHIM)
