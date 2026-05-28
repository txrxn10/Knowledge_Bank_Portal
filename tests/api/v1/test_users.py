import pytest
from app.schemas.user import UserCreate


def test_create_user(client):
    user_data = {
        "email": "test@example.com",
        "full_name": "Test User",
        "password": "testpassword123"
    }
    response = client.post("/api/v1/users", json=user_data)
    assert response.status_code == 201
    assert response.json()["email"] == user_data["email"]
    assert response.json()["full_name"] == user_data["full_name"]


def test_create_user_duplicate_email(client):
    user_data = {
        "email": "test@example.com",
        "full_name": "Test User",
        "password": "testpassword123"
    }
    # Create first user
    client.post("/api/v1/users", json=user_data)
    # Try to create duplicate
    response = client.post("/api/v1/users", json=user_data)
    assert response.status_code == 409


def test_get_user(client):
    # Create user first
    user_data = {
        "email": "test@example.com",
        "full_name": "Test User",
        "password": "testpassword123"
    }
    create_response = client.post("/api/v1/users", json=user_data)
    user_id = create_response.json()["id"]

    # Get user
    response = client.get(f"/api/v1/users/{user_id}")
    assert response.status_code == 200
    assert response.json()["email"] == user_data["email"]


def test_get_user_not_found(client):
    response = client.get("/api/v1/users/999")
    assert response.status_code == 404


def test_list_users(client):
    # Create multiple users
    for i in range(3):
        user_data = {
            "email": f"test{i}@example.com",
            "full_name": f"Test User {i}",
            "password": "testpassword123"
        }
        client.post("/api/v1/users", json=user_data)

    response = client.get("/api/v1/users")
    assert response.status_code == 200
    assert len(response.json()) == 3
