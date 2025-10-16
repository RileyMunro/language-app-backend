from pydantic import BaseModel, Field, ConfigDict
from datetime import datetime

# Word Schemas
class WordBase(BaseModel):
    vietnamese_word: str = Field(min_length=1, max_length=100)
    english_definition: str = Field(min_length=1)

class WordCreate(WordBase):
    pass

class WordResponse(WordBase):
    id: int
    created_at: datetime
    
    model_config = ConfigDict(from_attributes=True)


# Grammar Schemas
class GrammarBase(BaseModel):
    grammar_point: str = Field(min_length=1, max_length=200)
    english_explanation: str = Field(min_length=1)
    example_sentence: str | None = None

class GrammarCreate(GrammarBase):
    pass

class GrammarResponse(GrammarBase):
    id: int
    created_at: datetime
    
    model_config = ConfigDict(from_attributes=True)


# Question Schemas (for LLM output)
class Question(BaseModel):
    question_type: int = Field(ge=1, description="Type of question")
    question: str = Field(min_length=1)
    answers: list[str] = Field(min_length=2, max_length=6)
    correct_idx: int = Field(ge=0, description="Index of correct answer")
    
    model_config = ConfigDict(populate_by_name=True)
        
class QuestionGenerationRequest(BaseModel):
    num_questions: int = Field(default=5, ge=1, le=20)
    difficulty: str | None = Field(default=None, pattern="^(easy|medium|hard)$")

class QuestionGenerationResponse(BaseModel):
    questions: list[Question]