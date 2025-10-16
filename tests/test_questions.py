import pytest
from httpx import AsyncClient
from unittest.mock import AsyncMock, patch, Mock
from app.models import Word, Grammar
from app.schemas import Question


@pytest.mark.asyncio
async def test_generate_questions_no_data(client: AsyncClient) -> None:
    """Test generating questions without any words or grammar."""
    response = await client.post(
        "/api/v1/generate-questions",
        json={"num_questions": 3}
    )
    assert response.status_code == 400
    assert "No words or grammar found" in response.json()["detail"]


@pytest.mark.asyncio
@patch("app.openai_service.client.chat.completions.create", new_callable=AsyncMock)
async def test_generate_questions(
    mock_openai: AsyncMock,
    client: AsyncClient,
    sample_word: Word,
    sample_grammar: Grammar
) -> None:
    """Test generating questions with mocked OpenAI."""
    # Create a mock response object (not async)
    from unittest.mock import Mock
    
    mock_message = Mock()
    mock_message.content = '[{"question_type": 1, "question": "What does xin chào mean?", "answers": ["hello", "goodbye", "thank you"], "correct_idx": 0}]'
    
    mock_choice = Mock()
    mock_choice.message = mock_message
    
    mock_response = Mock()
    mock_response.choices = [mock_choice]
    
    # The AsyncMock itself is awaitable and returns the response
    mock_openai.return_value = mock_response
    
    response = await client.post(
        "/api/v1/generate-questions",
        json={"num_questions": 1}
    )
    
    assert response.status_code == 200
    data = response.json()
    assert "questions" in data
    assert len(data["questions"]) == 1
    assert data["questions"][0]["question"] == "What does xin chào mean?"
    assert data["questions"][0]["correct_idx"] == 0


@pytest.mark.asyncio
async def test_generate_questions_validation(client: AsyncClient) -> None:
    """Test question generation request validation."""
    response = await client.post(
        "/api/v1/generate-questions",
        json={"num_questions": 100}  # Exceeds max of 20
    )
    assert response.status_code == 422  # Validation error