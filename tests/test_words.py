import pytest
from httpx import AsyncClient
from app.models import Word


@pytest.mark.asyncio
async def test_create_word(client: AsyncClient) -> None:
    """Test creating a new word."""
    response = await client.post(
        "/api/v1/words",
        json={
            "vietnamese_word": "cảm ơn",
            "english_definition": "thank you"
        }
    )
    assert response.status_code == 201
    data = response.json()
    assert data["vietnamese_word"] == "cảm ơn"
    assert data["english_definition"] == "thank you"
    assert "id" in data
    assert "created_at" in data


@pytest.mark.asyncio
async def test_list_words_empty(client: AsyncClient) -> None:
    """Test listing words when database is empty."""
    response = await client.get("/api/v1/words")
    assert response.status_code == 200
    assert response.json() == []


@pytest.mark.asyncio
async def test_list_words(client: AsyncClient, sample_word: Word) -> None:
    """Test listing words."""
    response = await client.get("/api/v1/words")
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 1
    assert data[0]["vietnamese_word"] == "xin chào"


@pytest.mark.asyncio
async def test_get_word(client: AsyncClient, sample_word: Word) -> None:
    """Test getting a specific word."""
    response = await client.get(f"/api/v1/words/{sample_word.id}")
    assert response.status_code == 200
    data = response.json()
    assert data["vietnamese_word"] == "xin chào"
    assert data["english_definition"] == "hello"


@pytest.mark.asyncio
async def test_get_word_not_found(client: AsyncClient) -> None:
    """Test getting a non-existent word."""
    response = await client.get("/api/v1/words/9999")
    assert response.status_code == 404
    assert response.json()["detail"] == "Word not found"


@pytest.mark.asyncio
async def test_create_word_validation_error(client: AsyncClient) -> None:
    """Test creating a word with invalid data."""
    response = await client.post(
        "/api/v1/words",
        json={
            "vietnamese_word": "",  # Empty string should fail
            "english_definition": "hello"
        }
    )
    assert response.status_code == 422  # Validation error