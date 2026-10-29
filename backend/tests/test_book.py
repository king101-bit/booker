from tests.helpers import create_book, login_headers, make_admin_headers, make_user


def test_get_books_empty(client):
    response = client.get("/books")
    assert response.status_code == 200
    assert response.json() == {"books": []}


def test_delete_books(client):
    response = client.delete("/books/1")
    assert response.status_code == 401

def test_delete_book_without_token(client):
    response = client.delete("/books/1")
    assert response.status_code == 401


def test_delete_book_as_normal_user(client):
    make_user(client, "user@example.com", "pass12345")
    headers = login_headers(client, "user@example.com", "pass12345")
    assert create_book(client, headers).status_code == 201

    response = client.delete("/books/1", headers=headers)
    assert response.status_code == 403


def test_delete_book_as_admin(client, db_session):
    headers = make_admin_headers(client, db_session, "admin@example.com", "pass12345")
    assert create_book(client, headers).status_code == 201

    response = client.delete("/books/1", headers=headers)
    assert response.status_code == 204
    assert client.get("/books/1").status_code == 404
