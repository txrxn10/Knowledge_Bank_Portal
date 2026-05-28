# Knowledge Bank API

Enterprise-grade FastAPI application with repository pattern architecture.

## Project Structure

```
app/
├── api/v1/endpoints/       # API route handlers
├── core/                   # Security, exceptions, constants
├── models/                 # SQLAlchemy ORM models
├── schemas/                # Pydantic request/response models
├── repositories/           # Data access abstraction
│   ├── abstract/          # Repository interfaces
│   └── sql/               # SQLAlchemy implementations
├── services/              # Business logic
├── db/                    # Database configuration
└── utils/                 # Utilities (security, validators, etc)

tests/                      # Test suite mirroring app structure
```

## Quick Start

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. Create .env File

```bash
cp .env.example .env
```

### 3. Run the Application

```bash
uvicorn app.main:app --reload
```

The API will be available at `http://localhost:8000`

### 4. API Documentation

- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

## Running Tests

```bash
# Install dev dependencies
pip install -r requirements-dev.txt

# Run tests
pytest

# Run with coverage
pytest --cov=app
```

## Architecture Decisions

### Repository Pattern
- **Abstraction**: `app/repositories/abstract/` defines interfaces
- **Implementation**: `app/repositories/sql/` implements with SQLAlchemy
- **Benefits**: Easy to swap implementations (DB, cache, API) without changing endpoints

### Separation of Concerns
- **Endpoints**: HTTP routing only
- **Schemas**: Pydantic request/response validation
- **Models**: Database ORM definitions
- **Services**: Business logic
- **Repositories**: Data access

### Dependency Injection
- FastAPI `Depends()` injects repositories
- Easy to mock for testing
- Configuration centralized in `app/config.py`

## Adding a New Feature

### Example: Create a "Books" feature

1. **Create Model** (`app/models/book.py`)
```python
class Book(BaseModel):
    __tablename__ = "books"
    id = Column(Integer, primary_key=True)
    title = Column(String, nullable=False)
```

2. **Create Schema** (`app/schemas/book.py`)
```python
class BookCreate(BaseModel):
    title: str

class BookResponse(BookCreate):
    id: int
```

3. **Create Repository** 
   - Abstract: `app/repositories/abstract/book.py`
   - SQL: `app/repositories/sql/book.py`

4. **Create Endpoint** (`app/api/v1/endpoints/books.py`)
```python
@router.post("", response_model=BookResponse)
def create_book(book_in: BookCreate, repo: BookRepository = Depends(get_book_repository)):
    return repo.create(book_in)
```

5. **Add to Router** (update `app/api/v1/__init__.py`)

6. **Write Tests** (`tests/api/v1/test_books.py`)

## Development Workflow

### Code Quality

```bash
# Format code
black app tests

# Check imports
isort app tests

# Lint
flake8 app tests

# Type checking
mypy app
```

### Database Migrations

Using Alembic for migrations (optional setup):
```bash
alembic init migrations
alembic revision --autogenerate -m "Initial migration"
alembic upgrade head
```

## Configuration

All settings in `app/config.py` using Pydantic Settings:
- Load from `.env` file
- Override with environment variables
- Type-safe configuration

## Common Patterns

### Custom Repository Methods
```python
class UserRepository(BaseRepository[User]):
    @abstractmethod
    def get_by_email(self, email: str) -> Optional[User]:
        pass
```

### Service Layer
```python
class EmailService:
    def __init__(self, repo: UserRepository):
        self.repo = repo
    
    def send_welcome_email(self, user_id: int):
        user = self.repo.get(user_id)
        # Send email logic
```

### Exception Handling
```python
from app.core.exceptions import NotFoundException

if not user:
    raise NotFoundException("User not found")
```

## Contributing

1. Create feature branch
2. Add models → schemas → repositories → endpoints
3. Write tests
4. Run test suite and linters
5. Submit PR

## License

MIT
