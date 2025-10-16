from typing import List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.database import get_db
from app.models import Word, Grammar
from app.schemas import (
    WordCreate, WordResponse,
    GrammarCreate, GrammarResponse,
    QuestionGenerationRequest, QuestionGenerationResponse
)
from app.openai_service import generate_questions

router = APIRouter()

# Word endpoints
@router.post("/words", response_model=WordResponse, status_code=201)
async def create_word(
    word: WordCreate, 
    db: AsyncSession = Depends(get_db)
) -> Word:
    """Create a new word."""
    db_word = Word(**word.model_dump())
    db.add(db_word)
    await db.commit()
    await db.refresh(db_word)
    return db_word

@router.get("/words", response_model=List[WordResponse])
async def list_words(
    db: AsyncSession = Depends(get_db)
) -> List[Word]:
    """List all words."""
    result = await db.execute(select(Word))
    words = result.scalars().all()
    return list(words)

@router.get("/words/{word_id}", response_model=WordResponse)
async def get_word(
    word_id: int, 
    db: AsyncSession = Depends(get_db)
) -> Word:
    """Get a specific word by ID."""
    result = await db.execute(select(Word).where(Word.id == word_id))
    word = result.scalar_one_or_none()
    if not word:
        raise HTTPException(status_code=404, detail="Word not found")
    return word

# Grammar endpoints
@router.post("/grammar", response_model=GrammarResponse, status_code=201)
async def create_grammar(
    grammar: GrammarCreate, 
    db: AsyncSession = Depends(get_db)
) -> Grammar:
    """Create a new grammar point."""
    db_grammar = Grammar(**grammar.model_dump())
    db.add(db_grammar)
    await db.commit()
    await db.refresh(db_grammar)
    return db_grammar

@router.get("/grammar", response_model=List[GrammarResponse])
async def list_grammar(
    db: AsyncSession = Depends(get_db)
) -> List[Grammar]:
    """List all grammar points."""
    result = await db.execute(select(Grammar))
    grammar = result.scalars().all()
    return list(grammar)

@router.get("/grammar/{grammar_id}", response_model=GrammarResponse)
async def get_grammar(
    grammar_id: int, 
    db: AsyncSession = Depends(get_db)
) -> Grammar:
    """Get a specific grammar point by ID."""
    result = await db.execute(select(Grammar).where(Grammar.id == grammar_id))
    grammar = result.scalar_one_or_none()
    if not grammar:
        raise HTTPException(status_code=404, detail="Grammar not found")
    return grammar

# Question generation endpoint
@router.post("/generate-questions", response_model=QuestionGenerationResponse)
async def generate_questions_endpoint(
    request: QuestionGenerationRequest,
    db: AsyncSession = Depends(get_db)
) -> QuestionGenerationResponse:
    """Generate language learning questions based on known words and grammar."""
    # Fetch all words
    words_result = await db.execute(select(Word))
    words = words_result.scalars().all()
    
    # Fetch all grammar
    grammar_result = await db.execute(select(Grammar))
    grammar = grammar_result.scalars().all()
    
    # Check if we have enough data
    if not words and not grammar:
        raise HTTPException(
            status_code=400,
            detail="No words or grammar found. Please add some first."
        )
    
    # Convert to dicts for the service
    words_dict: List[dict[str, str]] = [
        {
            "vietnamese_word": w.vietnamese_word,
            "english_definition": w.english_definition
        }
        for w in words
    ]
    
    grammar_dict: List[dict[str, str | None]] = [
        {
            "grammar_point": g.grammar_point,
            "english_explanation": g.english_explanation,
            "example_sentence": g.example_sentence
        }
        for g in grammar
    ]
    
    # Generate questions
    questions = await generate_questions(
        words=words_dict,
        grammar=grammar_dict,
        num_questions=request.num_questions,
        difficulty=request.difficulty
    )
    
    return QuestionGenerationResponse(questions=questions)