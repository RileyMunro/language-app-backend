from sqlalchemy import String, Text
from sqlalchemy.orm import Mapped, mapped_column
from datetime import datetime, UTC
from app.database import Base

class Word(Base):
    __tablename__ = "words"
    
    id: Mapped[int] = mapped_column(primary_key=True)
    vietnamese_word: Mapped[str] = mapped_column(String(100), unique=True, index=True)
    english_definition: Mapped[str] = mapped_column(Text)
    created_at: Mapped[datetime] = mapped_column(default=lambda: datetime.now(UTC))
    
    def __repr__(self) -> str:
        return f"<Word {self.vietnamese_word}>"


class Grammar(Base):
    __tablename__ = "grammar"
    
    id: Mapped[int] = mapped_column(primary_key=True)
    grammar_point: Mapped[str] = mapped_column(String(200), unique=True, index=True)
    english_explanation: Mapped[str] = mapped_column(Text)
    example_sentence: Mapped[str | None] = mapped_column(Text, nullable=True)
    created_at: Mapped[datetime] = mapped_column(default=lambda: datetime.now(UTC))
    
    def __repr__(self) -> str:
        return f"<Grammar {self.grammar_point}>"