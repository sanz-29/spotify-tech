from datetime import datetime, timedelta, timezone

from jose import jwt

from app.config import ALGORITHM, SECRET_KEY


def test_registration_hashes_password_and_login_returns_bearer_token(client):
    registration = client.post(
        "/users/",
        json={
            "username": "listener",
            "email": "listener@example.com",
            "password": "password123",
        },
    )

    assert registration.status_code == 201
    body = registration.json()
    assert body["username"] == "listener"
    assert "password" not in body
    assert "password123" not in body

    login = client.post(
        "/users/login",
        json={"username": "listener", "password": "password123"},
    )

    assert login.status_code == 200
    token = login.json()
    assert token["token_type"] == "bearer"
    assert token["user_id"] == body["user_id"]
    assert "password" not in token
    assert client.get(
        "/users/me",
        headers={"Authorization": f"Bearer {token['access_token']}"},
    ).status_code == 200


def test_duplicate_registration_and_invalid_login_are_rejected(client):
    payload = {
        "username": "listener",
        "email": "listener@example.com",
        "password": "password123",
    }
    assert client.post("/users/", json=payload).status_code == 201
    assert client.post("/users/", json=payload).status_code == 409

    wrong_password = client.post(
        "/users/login",
        json={"username": "listener", "password": "wrong-password"},
    )
    unknown_user = client.post(
        "/users/login",
        json={"username": "missing", "password": "password123"},
    )
    assert wrong_password.status_code == 401
    assert unknown_user.status_code == 401


def test_missing_invalid_and_expired_tokens_return_401(client, user_factory):
    user = user_factory("listener", "listener@example.com")

    assert client.get("/users/me").status_code == 401
    assert client.get(
        "/users/me",
        headers={"Authorization": "Bearer not-a-token"},
    ).status_code == 401

    expired_token = jwt.encode(
        {
            "user_id": user.user_id,
            "exp": datetime.now(timezone.utc) - timedelta(minutes=1),
        },
        SECRET_KEY,
        algorithm=ALGORITHM,
    )
    response = client.get(
        "/users/me",
        headers={"Authorization": f"Bearer {expired_token}"},
    )
    assert response.status_code == 401
