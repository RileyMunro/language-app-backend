import pytest
from httpx import AsyncClient
from app.models import Grammar


@pytest.mark.asyncio
async def test_create_grammar(client: AsyncClient) -> None:
    """Test creating a new grammar point."""
    response = await client.post(
        "/api/v1/grammar",
        json={
            "grammar_point": "Không sao",
            "english_explanation": "No problem",
            "example_sentence": "Không sao đâu!"
        }
    )
    assert response.status_code == 201
    data = response.json()
    assert data["grammar_point"] == "Không sao"
    assert data["english_explanation"] == "No problem"
    assert data["example_sentence"] == "Không sao đâu!"


@pytest.mark.asyncio
async def test_create_grammar_without_example(client: AsyncClient) -> None:
    """Test creating grammar without example sentence."""
    response = await client.post(
        "/api/v1/grammar",
        json={
            "grammar_point": "Cái gì",
            "english_explanation": "What thing"
        }
    )
    assert response.status_code == 201
    data = response.json()
    assert data["example_sentence"] is None


@pytest.mark.asyncio
async def test_list_grammar(client: AsyncClient, sample_grammar: Grammar) -> None:
    """Test listing grammar points."""
    response = await client.get("/api/v1/grammar")
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 1
    assert data[0]["grammar_point"] == "phải không"


@pytest.mark.asyncio
async def test_get_grammar(client: AsyncClient, sample_grammar: Grammar) -> None:
    """Test getting a specific grammar point."""
    response = await client.get(f"/api/v1/grammar/{sample_grammar.id}")
    assert response.status_code == 200
    data = response.json()
    assert data["grammar_point"] == "phải không"


@pytest.mark.asyncio
async def test_get_grammar_not_found(client: AsyncClient) -> None:
    """Test getting a non-existent grammar point."""
    response = await client.get("/api/v1/grammar/9999")
    assert response.status_code == 404