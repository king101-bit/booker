# Booker

**Booker** is a RESTful API for managing books, authors and user accounts, built with Python and FastAPI.

The project was developed as a practical backend development exercise, focusing on REST API design, database integration, authentication, authorization, data validation and automated testing.

The backend is the primary focus of the project. A React frontend is also being developed, but is currently a work in progress.

## Features

- **Book Management:** Create, retrieve, update and delete books.
- **Author Management:** Create authors, retrieve their associated books and manage author records.
- **User Authentication:** Register users, hash passwords and authenticate using JWT access tokens.
- **Role-Based Authorization:** Restrict sensitive operations to users with administrator privileges.
- **Database Integration:** Persistent storage using SQLite and SQLAlchemy ORM.
- **Data Validation:** Request validation and response serialization using Pydantic.
- **Automated Testing:** Endpoint, authentication and authorization tests using pytest.

## Tech Stack

| Technology | Purpose |
|---|---|
| Python | Primary programming language |
| FastAPI | REST API framework |
| SQLite | Relational database |
| SQLAlchemy | Database ORM and queries |
| Pydantic | Data validation and serialization |
| Uvicorn | ASGI application server |
| PyJWT | JWT access token implementation |
| pwdlib | Password hashing |
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

Requires a valid bearer token.

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
| DELETE | `/authors/{author_id}` | Public | Delete an author |
| GET | `/authors/{author_id}/books` | Public | Retrieve books belonging to an author |

**Retrieve an author's books**

`GET /authors/{author_id}/books`

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

Author deletion is restricted when the author has associated books.

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

Passwords are hashed before being stored in the database.

**Login**

`POST /users/login`

Authentication uses OAuth2 password form data.

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
2. Passwords are hashed using `pwdlib` before being stored.
3. Users authenticate through the login endpoint.
4. Successful authentication generates a JWT access token.
5. Protected endpoints validate the bearer token before granting access.

Authorization is implemented separately from authentication through role-based access control.

The application distinguishes between authenticated users and administrators:

| Operation | Normal User | Administrator |
|---|---|---|
| Retrieve books | Allowed | Allowed |
| Create books | Allowed | Allowed |
| Update books | Forbidden | Allowed |
| Delete books | Forbidden | Allowed |
| Retrieve own profile | Allowed | Allowed |

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
| `409 Conflict` | Resource conflicts with existing database records or relationships |

## Database

Booker uses SQLite for persistent data storage and SQLAlchemy as its ORM.

The application contains three primary entities:

- **User:** Stores user information, hashed passwords and roles.
- **Author:** Stores author information.
- **Book:** Stores book information and references its associated author.

SQLAlchemy handles database interactions, while Pydantic schemas define the structure of incoming requests and outgoing responses.

## Testing

Automated tests are written using **pytest** and FastAPI's `TestClient`.

The test suite covers:

- User registration and authentication.
- Access to protected endpoints.
- Role-based authorization.
- Book creation and deletion.
- Administrator-only operations.
- Author-book relationships.
- Handling nonexistent resources.
- Database integrity constraints.

### Test Database

Tests use a separate in-memory SQLite database configured with SQLAlchemy's `StaticPool`.

FastAPI's database dependency is overridden during testing to ensure that test requests use the isolated database rather than the application's regular database.

Database tables are created before tests and dropped during fixture cleanup.

### Running Tests

From the backend directory, activate your virtual environment and run:

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

### Run the API

From the backend directory:

```bash
uvicorn app.main:app --reload
```

The API will be available at:

```text
http://localhost:8000
```

### Interactive API Documentation

FastAPI automatically generates interactive API documentation.

Once the server is running, visit:

- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

These interfaces allow you to inspect endpoints, view request and response schemas, and interact with the API.
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

**Backend:** Core API functionality, database integration, authentication, authorization and automated tests have been implemented.

**Frontend:** Work in progress. Development has primarily focused on the backend, with the React frontend being developed separately.

## Future Improvements

Potential areas for further development:

- Expand automated test coverage.
- Docker containerisation.
- Improved filtering, searching and pagination.
- Additional API features and validation.
- Frontend completion.
- Improved production configuration and deployment.

