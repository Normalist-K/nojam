# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Development Commands

### Development Server
```bash
# Run development server with auto-reload
python -m nojam.main
# Or directly with uvicorn
uvicorn nojam.main:app --host 0.0.0.0 --port 8000 --reload
```

### Testing
```bash
# Run all tests
pytest
# Run tests with asyncio support
pytest tests/
# Run specific test file
pytest tests/unit/test_quiz_service.py
# Run with coverage
pytest --cov=nojam
```

### Code Quality
```bash
# Lint code (configured in pyproject.toml)
ruff check .
# Format code
ruff format .
# Fix linting issues
ruff check --fix .
```

### Database
```bash
# Database file is automatically created as nojam.sqlite3 in project root
# No migration commands needed - using simple SQLite with aiosqlite
```

## Architecture Overview

### Core Structure
- **FastAPI Application**: Main entry point in `nojam/main.py`
- **JSON-Driven Quiz Platform**: Dynamic quiz system using JSON configuration files
- **Multi-Quiz Support**: Quiz selection homepage with different psychological tests
- **Pydantic v2**: All models use Pydantic v2 for validation and serialization

### Key Components

#### Quiz System (`nojam/models/quiz.py`)
- **JSON Schema v2.1**: Structured quiz definitions in `assets/schemas/quiz-schema-v2.1.json`
- **Quiz Models**: Complete Pydantic models for quiz metadata, questions, results
- **Scoring Methods**: Multiple scoring algorithms (simple_count, weighted_sum, percentage, mbti_dimensions)
- **Result Types**: Rich result cards with styling, descriptions, and sharing info

#### Services Layer
- **Quiz Loader** (`nojam/services/loader.py`): Loads quiz JSON files from `assets/quizzes/`
- **Quiz Service** (`nojam/services/quiz.py`): Result calculation with JSON-first approach, legacy fallback
- **Scoring Engine** (`nojam/services/scoring.py`): Handles different scoring methods including MBTI dimensions

#### Web Routes (`nojam/web/routes.py`)
- **Dynamic Quiz Rendering**: Forms generated from JSON quiz definitions
- **Multi-Quiz Support**: Homepage lists available quizzes
- **Result Calculation**: Supports both legacy and JSON-based quiz formats
- **Kakao Share Integration**: Social sharing functionality

#### Database (`nojam/db/repository.py`)
- **Simple SQLite**: Using aiosqlite for async database operations
- **Answer Storage**: Stores user responses with result types and metadata
- **No ORM**: Direct SQL queries for simplicity

### Quiz Configuration
- **Quiz Files**: Located in `assets/quizzes/` (e.g., `mind-age-test.json`, `mbti-5060-test.json`)
- **Schema Validation**: All quizzes validated against JSON Schema v2.1
- **Backward Compatibility**: Legacy hardcoded quizzes still supported as fallback

### Template System
- **Jinja2 Templates**: Located in `nojam/web/templates/`
- **Base Template**: Common layout with Kakao SDK integration
- **Dynamic Quiz Forms**: Generated from JSON quiz definitions
- **Result Cards**: Rich styling with gradients and social sharing

### Key Design Patterns
- **JSON-First Architecture**: All new quizzes use JSON configuration
- **Graceful Fallback**: Legacy hardcoded logic maintained for compatibility
- **Scoring Abstraction**: Multiple scoring methods supported through unified interface
- **Async/Await**: Throughout for database and web operations

### Dependencies
- **FastAPI**: Web framework
- **Pydantic v2**: Data validation and serialization
- **aiosqlite**: Async SQLite database
- **structlog**: Structured logging
- **Jinja2**: Template engine
- **Ruff**: Code linting and formatting
- **pytest**: Testing framework with asyncio support