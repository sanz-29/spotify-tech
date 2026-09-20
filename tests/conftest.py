import os
from collections.abc import Iterator

import pytest
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session, sessionmaker


os.environ["DATABASE_URL"] = "sqlite:///./.pytest_test.db"
os.environ["SECRET_KEY"] = "test-secret-key-for-spotify-tech"
os.environ["ALGORITHM"] = "HS256"
os.environ["ACCESS_TOKEN_EXPIRE_MINUTES"] = "30"
os.environ["ALLOWED_ORIGINS"] = "http://testserver"

from app.app import app
from app.database import Base, engine, get_db
from app.security import hash_password
from app.models.user import User


TestingSessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    expire_on_commit=False,
    bind=engine,
)


def override_get_db() -> Iterator[Session]:
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()


app.dependency_overrides[get_db] = override_get_db


@pytest.fixture(autouse=True)
def reset_database() -> Iterator[None]:
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)


@pytest.fixture
def client() -> Iterator[TestClient]:
    with TestClient(app) as test_client:
        yield test_client


@pytest.fixture
def db() -> Iterator[Session]:
    session = TestingSessionLocal()
    try:
        yield session
    finally:
        session.close()


def create_user(
    db: Session,
    username: str,
    email: str,
    role: str = "user",
) -> User:
    user = User(
        username=username,
        email=email,
        password=hash_password("password123"),
        role=role,
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    return user


@pytest.fixture
def user_factory(db: Session):
    def factory(
        username: str,
        email: str,
        role: str = "user",
    ) -> User:
        return create_user(db, username, email, role)

    return factory


@pytest.fixture
def auth_headers():
    def get_headers(client: TestClient, username: str, password: str):
        response = client.post(
            "/users/login",
            json={"username": username, "password": password},
        )
        assert response.status_code == 200
        return {"Authorization": f"Bearer {response.json()['access_token']}"}

    return get_headers
