# Knowledge Bank API - Project Guide

## Overview
Enterprise-grade FastAPI application using the repository pattern for data access abstraction.

## Architecture Layers

### 1. **API Layer** (`app/api/v1/endpoints/`)
- HTTP route handlers
- Request validation (Pydantic schemas)
- Response models
- Exception handling

### 2. **Repository Layer** (`app/repositories/`)
- **Abstract** (`abstract/`): Interface definitions
- **SQL** (`sql/`): SQLAlchemy implementations
- Abstracts data access, enables swapping implementations
- CRUD operations + custom queries

### 3. **Schema Layer** (`app/schemas/`)
- Pydantic models for request/response validation
- Separate from ORM models (flexibility)
- Validation rules and constraints

### 4. **Model Layer** (`app/models/`)
- SQLAlchemy ORM definitions
- Database schema
- Inherits from `BaseModel` with created_at/updated_at

### 5. **Service Layer** (`app/services/`)
- Business logic (notifications, emails, external APIs)
- Can use repositories and other services
- Reusable across endpoints

### 6. **Core Layer** (`app/core/`)
- **exceptions.py**: Custom HTTP exceptions
- **security.py**: Auth, JWT, password hashing
- **constants.py**: App-wide constants

### 7. **Database Layer** (`app/db/`)
- **base.py**: SQLAlchemy declarative base
- **session.py**: Database session management

### 8. **Utils** (`app/utils/`)
- Helpers, validators, decorators
- Security utilities (hashing, JWT)

## Key Files

| File | Purpose |
|------|---------|
| `app/config.py` | Configuration management (Pydantic Settings) |
| `app/main.py` | FastAPI app initialization, middleware, routes |
| `app/dependencies.py` | Dependency injection setup (Depends) |
| `requirements.txt` | Production dependencies |
| `requirements-dev.txt` | Development dependencies (pytest, black, etc) |
| `pyproject.toml` | Project metadata, tool configs |
| `.env.example` | Environment variable template |
| `tests/conftest.py` | Pytest fixtures, test client setup |

## How to Add Features

### Example: Create a "Products" feature

```
1. Create Model:
   app/models/product.py
   - SQLAlchemy table definition

2. Create Schema:
   app/schemas/product.py
   - ProductCreate, ProductResponse Pydantic models

3. Create Repository:
   app/repositories/abstract/product.py - interface
   app/repositories/sql/product.py - SQLAlchemy impl

4. Create Endpoint:
   app/api/v1/endpoints/products.py
   - @router.post, @router.get, etc using repo

5. Register Endpoint:
   app/api/v1/__init__.py - include_router

6. Write Tests:
   tests/api/v1/test_products.py
   - Test happy path + edge cases
```

## Testing Strategy

### Test Structure
- Mirror `app/` in `tests/`
- `tests/conftest.py`: Pytest fixtures (db, client)
- Unit tests: Repository, service logic
- Integration tests: API endpoints with test DB

### Run Tests
```bash
pytest                          # Run all
pytest tests/api/v1/            # Run endpoint tests
pytest --cov=app                # With coverage
```

## Development Workflow

```bash
# Install dependencies
pip install -r requirements-dev.txt

# Format code
black app tests

# Check imports
isort app tests

# Run tests
pytest

# Start API
uvicorn app.main:app --reload
```

## Database Workflows

### Using SQLite (default, development)
- Auto-created at `test.db`
- No setup needed

### Using PostgreSQL (production)
- Update `DATABASE_URL` in `.env`
- Example: `postgresql://user:pass@localhost:5432/db_name`
- Use docker-compose: `docker-compose up`

### Migrations (Optional)
- Use Alembic for schema versioning
- Already scaffolded in `migrations/`

## Configuration

### Loading Configuration
1. `.env` file (checked first)
2. Environment variables (override .env)
3. Default values in `app/config.py`

### Common Settings
- `DEBUG`: Enable debug mode
- `DATABASE_URL`: Database connection string
- `SECRET_KEY`: JWT secret (change in production!)
- `CORS_ORIGINS`: Allowed CORS origins
- `API_V1_STR`: API prefix (/api/v1)

## Dependency Injection Pattern

### Usage
```python
def get_user_repository(db: Session = Depends(get_db)) -> UserRepository:
    return SQLUserRepository(db)

@router.post("/users")
def create_user(user: UserCreate, repo: UserRepository = Depends(get_user_repository)):
    return repo.create_with_password(...)
```

### Benefits
- Easy to test (inject mock repo)
- Decoupled endpoints from implementation
- FastAPI handles dependency resolution

## Exception Handling

### Custom Exceptions
Located in `app/core/exceptions.py`:
- `NotFoundException` (404)
- `ValidationException` (422)
- `UnauthorizedException` (401)
- `ForbiddenException` (403)
- `ConflictException` (409)

### Usage
```python
if not user:
    raise NotFoundException("User not found")
if existing_user:
    raise ConflictException("Email already registered")
```

## API Versioning

- Current version: `v1` in `app/api/v1/`
- Future versions go in `app/api/v2/`, `v3/`, etc
- Allows backward compatibility while evolving API

## Docker

### Development
```bash
docker-compose up
```
- Starts FastAPI on port 8000
- PostgreSQL on port 5432
- Auto-reload enabled

### Production
- Use environment variables for config
- Set `DEBUG=False`
- Use production secret key
- Consider using Gunicorn instead of Uvicorn

## Common Pitfalls to Avoid

1. **Mixing business logic in endpoints**: Use services or repositories
2. **Tight coupling to ORM**: Use repositories as abstraction
3. **Validation in multiple places**: Use Pydantic schemas
4. **Hardcoded config**: Use app/config.py
5. **Not testing edge cases**: Always test 400, 404, 409 responses
