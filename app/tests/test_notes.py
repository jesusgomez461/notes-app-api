import pytest


@pytest.mark.asyncio
async def test_create_note_success(async_client):
    await async_client.post(
        "/api/auth/register",
        json={
            "document": "12345678",
            "full_name": "Test User",
            "email": "test@example.com",
            "password": "password123",
        },
    )
    login_response = await async_client.post(
        "/api/auth/login",
        json={"email": "test@example.com", "password": "password123"},
    )
    token = login_response.json()["access_token"]

    response = await async_client.post(
        "/api/notes/",
        headers={"Authorization": f"Bearer {token}"},
        json={"title": "Test Note", "content": "This is a test note"},
    )
    assert response.status_code == 200
    data = response.json()
    assert data["title"] == "Test Note"
    assert data["content"] == "This is a test note"
