from app import models


def make_user(client, email, password):
    return client.post("/users", json={"email": email, "password": password})


def login_headers(client, email, password):
    response = client.post(
        "/users/login", data={"username": email, "password": password}
    )
    token = response.json()["access_token"]
    return {"Authorization": f"Bearer {token}"}


def make_admin_headers(client, db_session, email, password):
    make_user(client, email, password)
    user = db_session.query(models.User).filter(models.User.email == email).first()
    user.role = "admin"
    db_session.commit()
    return login_headers(client, email, password)


def create_book(client, headers):
    client.post("/authors", json={"name": "Orwell"})
    return client.post(
        "/books",
        json={"title": "Animal Farm", "price": 9.99, "author_id": 1},
        headers=headers,
    )