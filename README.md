# Booker

**Booker** is a RESTful API for managing books, authors and user accounts, built with Python and FastAPI.

The project was developed as a practical backend development exercise, focusing on REST API design, database integration, migrations, authentication, authorization, data validation and automated testing.

The backend is the primary focus of the project. A React frontend is also being developed, but is currently a work in progress.

## Features

- **Book Management:** Create, retrieve, update and delete books.
- **Author Management:** Create authors, retrieve their associated books and delete authors (blocked while they still have books).
- **User Authentication:** Register users, hash passwords and authenticate using JWT access tokens.
- **Role-Based Authorization:** Restrict sensitive operations to users with administrator privileges.
- **Database Integration:** Persistent storage using SQLite and SQLAlchemy ORM.
- **Schema Migrations:** Versioned database changes managed with Alembic.
- **Configuration via Environment:** Secrets and database settings loaded from `.env` using pydantic-settings.
- **Data Validation:** Request validation and response serialization using Pydantic.
- **Automated Testing:** Endpoint, authentication and authorization tests using pytest.

## Tech Stack

| Technology | Purpose |
|---|---|
| Python | Primary programming language |
| FastAPI | REST API framework |
| SQLite | Relational database |
| SQLAlchemy | Database ORM and queries |
| Alembic | Database migrations |
| Pydantic / pydantic-settings | Data validation, serialization and configuration |
| Uvicorn | ASGI application server |
| PyJWT | JWT access token implementation |
| pwdlib (Argon2) | Password hashing |
| Pytest | Automated testing |
| React | Frontend (work in progress) |
| Axios | Frontend HTTP client |

## API Reference

All endpoints return JSON responses unless otherwise specified.

### Books

| Method | Endpoint | Access | Description |
|---|---|---|---|
| GET | `/books` | Public | Retrieve all books |
| POST | `/books` | Authenticated | Create a book |
| GET | `/books/{book_id}` | Public | Retrieve a book by ID |
| PUT | `/books/{book_id}` | Admin | Update a book |
| DELETE | `/books/{book_id}` | Admin | Delete a book |

**Create a book**

`POST /books`

Requires a valid bearer token. Returns `404` if `author_id` does not exist.

Request:

```json
{
  "title": "Animal Farm",
  "author_id": 1,
  "price": 11.99
}
```

Response (`201 Created`):

```json
{
  "id": 2,
  "title": "Animal Farm",
  "author": {
    "id": 1,
    "name": "George Orwell"
  },
  "price": 11.99
}
```

**Retrieve all books**

`GET /books`

Response (`200 OK`):

```json
{
  "books": [
    {
      "id": 1,
      "title": "1984",
      "author": {
        "id": 1,
        "name": "George Orwell"
      },
      "price": 12.99
    },
    {
      "id": 2,
      "title": "Animal Farm",
      "author": {
        "id": 1,
        "name": "George Orwell"
      },
      "price": 11.99
    }
  ]
}
```

### Authors

| Method | Endpoint | Access | Description |
|---|---|---|---|
| POST | `/authors` | Public | Create an author |
| DELETE | `/authors/{author_id}` | Admin | Delete an author |
| GET | `/authors/{author_id}/books` | Public | Retrieve books belonging to an author |

Creating an author whose name already exists returns `409 Conflict`.

**Retrieve an author's books**

`GET /authors/{author_id}/books`

Returns `404` if the author does not exist, and an empty list if the author exists but has no books.

Response (`200 OK`):

```json
{
  "books": [
    {
      "id": 1,
      "title": "1984",
      "author": {
        "id": 1,
        "name": "George Orwell"
      },
      "price": 12.99
    }
  ]
}
```

Author deletion is blocked when the author has associated books.

Response (`409 Conflict`):

```json
{
  "detail": "Author has books, delete or reassign them first"
}
```

### Users and Authentication

| Method | Endpoint | Access | Description |
|---|---|---|---|
| POST | `/users` | Public | Register a new user |
| POST | `/users/login` | Public | Authenticate and obtain a JWT |
| GET | `/users/me` | Authenticated | Retrieve the current user's information |

**Register a user**

`POST /users`

Request:

```json
{
  "email": "user@example.com",
  "password": "your-password"
}
```

Response (`201 Created`):

```json
{
  "id": 3,
  "email": "user@example.com"
}
```

Passwords are hashed before being stored in the database. Registering an email that already exists returns `409 Conflict`. New accounts always receive the `user` role; signup never accepts a role from the request.

**Login**

`POST /users/login`

Authentication uses OAuth2 password form data. The email goes in the `username` field.

Request (`application/x-www-form-urlencoded`):

```text
username=user@example.com
password=your-password
```

Response (`200 OK`):

```json
{
  "access_token": "<your-access-token>",
  "token_type": "bearer"
}
```

Wrong email or wrong password returns `401` with the same message for both, so the API does not reveal which emails are registered.

**Retrieve the current user**

`GET /users/me`

Requires a valid JWT access token.

Include the token in the request header:

```http
Authorization: Bearer <your-access-token>
```

Response (`200 OK`):

```json
{
  "id": 3,
  "email": "user@example.com"
}
```

## Authentication and Authorization

Booker implements JWT-based authentication using the OAuth2 password flow.

The authentication process consists of:

1. Users register with an email address and password.
2. Passwords are hashed with Argon2 (via `pwdlib`) before being stored.
3. Users authenticate through the login endpoint.
4. Successful authentication generates a signed JWT access token that expires after 30 minutes.
5. Protected endpoints validate the bearer token before granting access.

Authorization is implemented separately from authentication through role-based access control.

| Operation | Normal User | Administrator |
|---|---|---|
| Retrieve books | Allowed | Allowed |
| Create books | Allowed | Allowed |
| Update books | Forbidden | Allowed |
| Delete books | Forbidden | Allowed |
| Delete authors | Forbidden | Allowed |
| Retrieve own profile | Allowed | Allowed |

### Creating an administrator

There is deliberately no API for becoming an admin. Promote a user directly in the database after they register:

```bash
sqlite3 book.db "UPDATE users SET role='admin' WHERE email='you@example.com';"
```

## Error Handling

The API uses HTTP status codes to communicate request outcomes.

| Status Code | Description |
|---|---|
| `200 OK` | Request completed successfully |
| `201 Created` | Resource successfully created |
| `204 No Content` | Resource successfully deleted |
| `401 Unauthorized` | Authentication required or credentials invalid |
| `403 Forbidden` | Authenticated user lacks the required permissions |
| `404 Not Found` | Requested resource does not exist |
| `409 Conflict` | Resource conflicts with existing records (duplicate email or author, author still has books) |
| `422 Unprocessable Entity` | Request body or parameters failed validation |

## Database

Booker uses SQLite for persistent data storage and SQLAlchemy as its ORM. Schema changes are managed with Alembic migrations.

The application contains three primary entities:

- **User:** Stores email, hashed password and role.
- **Author:** Stores the author's name (unique).
- **Book:** Stores title, price and a foreign key to its author (one author has many books).

SQLAlchemy handles database interactions, while Pydantic schemas define the structure of incoming requests and outgoing responses.

## Configuration

Settings are read from a `.env` file in the `backend/` directory. Copy the example file and fill it in:

```bash
cp .env.example .env
```

| Variable | Description |
|---|---|
| `SECRET_KEY` | Required. Secret used to sign JWTs. Generate one with `python -c "import secrets; print(secrets.token_hex(32))"` |
| `DATABASE_URL` | Optional. Defaults to `sqlite:///./book.db` |

Never commit `.env`. Anyone with the `SECRET_KEY` can forge login tokens.

## Testing

Automated tests are written using **pytest** and FastAPI's `TestClient`.

The test suite currently covers:

- Listing books and an author's books when none exist.
- `404` for an author that does not exist.
- User registration and login helpers.
- Delete authorization for books with three callers: no token (`401`), normal user (`403`) and administrator (`204`).

More coverage is planned (see Future Improvements).

### Test Database

Tests use a separate in-memory SQLite database configured with SQLAlchemy's `StaticPool`.

FastAPI's database dependency is overridden during testing so test requests use the isolated database rather than the application's regular database.

Database tables are created before each test and dropped afterward, so every test starts empty.

### Running Tests

From the backend directory, with your virtual environment activated:

```bash
pytest
```

## Getting Started

### Prerequisites

- Python 3.10 or newer
- pip
- Git
- Node.js and npm (for the frontend)

### Clone the Repository

```bash
git clone https://github.com/king101-bit/booker.git
cd booker
```

### Backend Setup

Navigate to the backend directory:

```bash
cd backend
```

Create a virtual environment:

```bash
python -m venv .venv
```

Activate it:

**Linux/macOS**

```bash
source .venv/bin/activate
```

**Windows**

```powershell
.venv\Scripts\activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

Create your configuration file (see [Configuration](#configuration)):

```bash
cp .env.example .env
```

Then set a real `SECRET_KEY` in `.env`.

Create the database tables:

```bash
alembic upgrade head
```

### Run the API

From the backend directory:

```bash
uvicorn app.main:app --reload
```

The API will be available at:

```text
http://localhost:8000
```

### Database Migrations

After changing a model in `app/models.py`:

```bash
alembic revision --autogenerate -m "describe the change"
alembic upgrade head
```

Read the generated script in `alembic/versions/` before running it.

### Interactive API Documentation

FastAPI automatically generates interactive API documentation.

Once the server is running, visit:

- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

These interfaces allow you to inspect endpoints, view request and response schemas, and interact with the API. To call protected routes, click **Authorize** in Swagger UI and log in with your email as the username.

Swagger UI looks like this:
<img width="1919" height="1087" alt="image" src="https://github.com/user-attachments/assets/dae14556-f82b-4bc4-b69c-852cff3257ee" />

### Frontend Setup

The React frontend is currently a work in progress.

Navigate to the frontend directory:

```bash
cd frontend
```

Install dependencies and start the development server:

```bash
npm install
npm run dev
```

## Project Status

**Backend:** Core API functionality, database integration, migrations, authentication, authorization and a first set of automated tests have been implemented.

**Frontend:** Work in progress. Development has primarily focused on the backend, with the React frontend being developed separately.

## Future Improvements

- Expand test coverage (PUT, duplicate email and author conflicts, wrong password, invalid `author_id`).
- Search, filtering, sorting and offset-based pagination.
- Migrate from SQLite to PostgreSQL.
- Docker containerisation and CI.
- Email format validation and login rate limiting.
- Frontend completion.
- Production configuration and deployment.
