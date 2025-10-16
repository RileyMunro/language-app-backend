import pytest
from typing import AsyncGenerator, Generator
from httpx import AsyncClient, ASGITransport
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from app.main import app
from app.database import Base, get_db
from app.models import Word, Grammar

# Use in-memory SQLite for tests
TEST_DATABASE_URL = "sqlite+aiosqlite:///:memory:"

test_engine = create_async_engine(TEST_DATABASE_URL, echo=True)
test_async_session = async_sessionmaker(
    test_engine, class_=AsyncSession, expire_on_commit=False
)


async def override_get_db() -> AsyncGenerator[AsyncSession, None]:
    """Override the get_db dependency for tests."""
    async with test_async_session() as session:
        yield session


@pytest.fixture(scope="function")
async def db_session() -> AsyncGenerator[AsyncSession, None]:
    """Create a fresh database for each test."""
    async with test_engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    
    async with test_async_session() as session:
        yield session
    
    async with test_engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)


@pytest.fixture(scope="function")
async def client(db_session: AsyncSession) -> AsyncGenerator[AsyncClient, None]:
    """Create a test client with database dependency override."""
    app.dependency_overrides[get_db] = override_get_db
    
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        yield ac
    
    app.dependency_overrides.clear()


@pytest.fixture
async def sample_word(db_session: AsyncSession) -> Word:
    """Create a sample word for testing."""
    word = Word(
        vietnamese_word="xin chào",
        english_definition="hello"
    )
    db_session.add(word)
    await db_session.commit()
    await db_session.refresh(word)
    return word


@pytest.fixture
async def sample_grammar(db_session: AsyncSession) -> Grammar:
    """Create a sample grammar point for testing."""
    grammar = Grammar(
        grammar_point="phải không",
        english_explanation="Tag question meaning 'right?'",
        example_sentence="Em là người Mỹ, phải không?"
    )
    db_session.add(grammar)
    await db_session.commit()
    await db_session.refresh(grammar)
    return grammar