def test_get_author_books_empty(client):
    client.post("/authors", json={"name": "Orwell"})
    response = client.get("/authors/1/books")
    assert response.status_code == 200
    assert response.json() == {"books": []}


def test_get_author_books_missing_author(client):
    response = client.get("/authors/999/books")
    assert response.status_code == 404