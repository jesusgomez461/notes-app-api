import pytest


@pytest.mark.asyncio
async def test_login_success(async_client):
    response = await async_client.post(
        "/api/auth/register",
        json={
            "document": "12345678",
            "full_name": "Test User",
            "email": "test@example.com",
            "password": "password123",
        },
    )
    assert response.status_code == 200

    response = await async_client.post(
        "/api/auth/login",
        json={"email": "test@example.com", "password": "password123"},
    )
    assert response.status_code == 200
    assert "access_token" in response.json()
