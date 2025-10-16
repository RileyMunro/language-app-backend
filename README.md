# Language Learning App - Backend

A FastAPI-based backend for generating Vietnamese language learning questions using AI. The app uses known words and grammar points to create personalized multiple-choice quiz questions.

## Features

- 📚 Store and manage Vietnamese vocabulary with English definitions
- 📝 Track grammar points with explanations and examples
- 🤖 Generate AI-powered quiz questions using OpenAI
- 🐳 Docker-ready with Poetry for dependency management
- ✅ Fully typed with mypy and tested with pytest
- 🗄️ SQLite database with async SQLAlchemy

## Tech Stack

- **FastAPI** - Modern, fast web framework
- **SQLAlchemy 2.0** - Async ORM
- **OpenAI API** - Question generation
- **Poetry** - Dependency management
- **Docker** - Containerization
- **Pydantic** - Data validation
- **pytest** - Testing

## Setup

### Prerequisites

- Python 3.11+
- Poetry
- Docker & Docker Compose (for containerized deployment)
- OpenAI API key

### Installation

1. **Clone the repository:**
```bash
git clone https://github.com/RileyMunro/language-app-backend.git
cd backend
```

2. **Install dependencies:**
```bash
poetry install
```

3. **Create `.env` file:**
```bash
OPENAI_API_KEY=your-openai-api-key-here
DATABASE_URL=sqlite+aiosqlite:///./app.db
```

4. **Seed the database (optional):**
```bash
poetry run python -m app.db_seeder
```

This will populate the database with 95+ Vietnamese words and 23 grammar points.

## Running the App

### Using Docker (Recommended)
```bash
docker-compose up --build
```

The API will be available at `http://localhost:8001`

### Using Poetry (Local Development)
```bash
poetry run uvicorn app.main:app --reload
```

The API will be available at `http://localhost:8000`

## API Documentation

Once running, visit:
- **Swagger UI**: `http://localhost:8001/docs`
- **ReDoc**: `http://localhost:8001/redoc`

## API Endpoints

### Words

#### Add a Word
```bash
POST /api/v1/words
```
```json
{
  "vietnamese_word": "xin chào",
  "english_definition": "hello"
}
```

#### List All Words
```bash
GET /api/v1/words
```

#### Get Specific Word
```bash
GET /api/v1/words/{word_id}
```

### Grammar

#### Add Grammar Point
```bash
POST /api/v1/grammar
```
```json
{
  "grammar_point": "phải không",
  "english_explanation": "Tag question meaning 'right?'",
  "example_sentence": "Em là người Mỹ, phải không?"
}
```

Note: `example_sentence` is optional.

#### List All Grammar
```bash
GET /api/v1/grammar
```

#### Get Specific Grammar Point
```bash
GET /api/v1/grammar/{grammar_id}
```

### Question Generation

#### Generate Questions
```bash
POST /api/v1/generate-questions
```
```json
{
  "num_questions": 5,
  "difficulty": "medium"
}
```

**Parameters:**
- `num_questions` (optional): Number of questions (1-20, default: 5)
- `difficulty` (optional): "easy", "medium", or "hard"

**Response:**
```json
{
  "questions": [
    {
      "question_type": 1,
      "question": "What does 'xin chào' mean?",
      "answers": ["hello", "goodbye", "thank you", "please"],
      "correct_idx": 0
    }
  ]
}
```

## Development

### Running Tests
```bash
poetry run pytest
```

**With coverage:**
```bash
poetry run pytest --cov=app
```

**Verbose output:**
```bash
poetry run pytest -v
```

### Type Checking
```bash
poetry run mypy app/
```

### Code Structure
```
backend/
├── app/
│   ├── __init__.py
│   ├── main.py              # FastAPI application
│   ├── config.py            # Settings/configuration
│   ├── database.py          # Database setup
│   ├── models.py            # SQLAlchemy models
│   ├── schemas.py           # Pydantic schemas
│   ├── routes.py            # API endpoints
│   ├── openai_service.py    # OpenAI integration
│   └── db_seeder.py         # Database seeding script
├── tests/
│   ├── conftest.py          # Pytest fixtures
│   ├── test_words.py
│   ├── test_grammar.py
│   ├── test_questions.py
│   └── test_health.py
├── docker-compose.yml
├── Dockerfile
├── pyproject.toml
├── pytest.ini
└── README.md
```

### Adding New Words/Grammar

**Option 1: Via API (Swagger UI)**
1. Navigate to `http://localhost:8001/docs`
2. Use the POST endpoints to add data interactively

**Option 2: Via curl**
```bash
# Add a word
curl -X POST "http://localhost:8001/api/v1/words" \
  -H "Content-Type: application/json" \
  -d '{"vietnamese_word": "cảm ơn", "english_definition": "thank you"}'

# Add grammar
curl -X POST "http://localhost:8001/api/v1/grammar" \
  -H "Content-Type: application/json" \
  -d '{
    "grammar_point": "Không sao",
    "english_explanation": "Expression meaning no problem",
    "example_sentence": "Không sao đâu!"
  }'
```

**Option 3: Bulk Seed**

Edit `app/db_seeder.py` to add your words/grammar to the `WORDS` and `GRAMMAR` lists, then run:
```bash
poetry run python -m app.db_seeder
```

### Resetting the Database
```bash
rm app.db
poetry run python -m app.db_seeder
```

## Environment Variables

| Variable | Description | Default |
|----------|-------------|---------|
| `OPENAI_API_KEY` | Your OpenAI API key | Required |
| `DATABASE_URL` | Database connection string | `sqlite+aiosqlite:///./app.db` |

## Docker

### Build Image
```bash
docker-compose build
```

### View Logs
```bash
docker-compose logs -f
```

### Stop Services
```bash
docker-compose down
```

## Language Focus

This app is specifically designed for **Southern Vietnamese dialect**. The vocabulary and grammar patterns reflect conversational Southern Vietnamese usage.

## License

MIT

## Contact

Riley Munro - riley.munro@gmail.com

## Acknowledgments

- README documentation generated with assistance from Claude (Anthropic)
- OpenAI for question generation API
