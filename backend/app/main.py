import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .routers import authors, books, users

# models.Base.metadata.create_all(bind=engine)

app = FastAPI(
   title="Booker API",
   description="A RESTful API for managing books, authors and user accounts.",
   version="1.0.0")
app.include_router(books.router)
app.include_router(authors.router)
app.include_router(users.router)

origins = ["http://localhost:5173"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
