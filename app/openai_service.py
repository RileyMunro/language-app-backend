from typing import List, Dict, Optional
from openai import AsyncOpenAI
from app.config import settings
from app.schemas import Question
import json

client: AsyncOpenAI = AsyncOpenAI(api_key=settings.openai_api_key)

async def generate_questions(
    words: List[Dict[str, str]],
    grammar: List[Dict[str, Optional[str]]],
    num_questions: int = 5,
    difficulty: Optional[str] = None
) -> List[Question]:
    """
    Generate language learning questions using OpenAI.
    
    Args:
        words: List of dictionaries containing vietnamese_word and english_definition
        grammar: List of dictionaries containing grammar_point, english_explanation, and example_sentence
        num_questions: Number of questions to generate
        difficulty: Optional difficulty level (easy, medium, hard)
    
    Returns:
        List of Question objects
    """
    # Build the prompt
    words_str: str = "\n".join([
        f"- {w['vietnamese_word']}: {w['english_definition']}" 
        for w in words
    ])
    grammar_str: str = "\n".join([
        f"- {g['grammar_point']}: {g['english_explanation']}" + 
        (f" (Example: {g['example_sentence']})" if g.get('example_sentence') else "")
        for g in grammar
    ])
    
    difficulty_note: str = f"\nDifficulty level: {difficulty}" if difficulty else ""
    
    prompt: str = f"""You are a Vietnamese language teacher creating quiz questions.

Known Words:
{words_str}

Known Grammar:
{grammar_str}
{difficulty_note}

Create {num_questions} multiple-choice questions that test the student's understanding of these words and grammar points.
Each question should have 2-6 answer choices with exactly one correct answer.

Return ONLY valid JSON in this exact format:
[
  {{
    "question_type": 1,
    "question": "What does 'xin chào' mean?",
    "answers": ["Hello", "Goodbye", "Thank you", "Please"],
    "correct_idx": 0
  }}
]
"""
    
    response = await client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {
                "role": "system", 
                "content": "You are a helpful Vietnamese language teacher. You always respond with valid JSON."
            },
            {"role": "user", "content": prompt}
        ],
        response_format={"type": "json_object"},
        temperature=0.7
    )
    
    # Parse the response
    content: str = response.choices[0].message.content or "[]"
    questions_data: List[Dict] | Dict = json.loads(content)
    
    # Handle both array and object responses
    if isinstance(questions_data, dict) and "questions" in questions_data:
        questions_data = questions_data["questions"]
    
    # Validate with Pydantic
    questions: List[Question] = [Question(**q) for q in questions_data]
    
    return questions