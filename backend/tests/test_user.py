from tests.helpers import login_headers, make_user


def test_helpers_work(client):
    make_user(client, "test@example.com", "testpass123")
    headers = login_headers(client, "test@example.com", "testpass123")
    assert "Authorization" in headers
