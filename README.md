# Telegram Bot Project

A modern, scalable Telegram bot built with Python, following best practices for development and deployment.

## Features

- 🚀 Asynchronous architecture using python-telegram-bot
- 🗄️ Database integration with SQLAlchemy and Alembic migrations
- 🔒 Environment-based configuration management
- 🧪 Comprehensive testing setup with pytest
- 📝 Type hints and static analysis with mypy
- 🎨 Code formatting with black and isort
- 📊 Logging and monitoring with structlog
- 🔧 Development tools and pre-commit hooks
- 📚 Documentation with Sphinx

## Project Structure

```
telegram-bot/
├── src/
│   └── bot/
│       ├── __init__.py
│       ├── main.py              # Bot entry point
│       ├── config.py            # Configuration management
│       ├── handlers/            # Command and message handlers
│       │   ├── __init__.py
│       │   ├── commands.py
│       │   └── messages.py
│       ├── models/              # Database models
│       │   ├── __init__.py
│       │   ├── base.py
│       │   └── user.py
│       ├── services/            # Business logic
│       │   ├── __init__.py
│       │   └── user_service.py
│       ├── utils/               # Utility functions
│       │   ├── __init__.py
│       │   ├── logging.py
│       │   └── helpers.py
│       └── middleware/          # Custom middleware
│           ├── __init__.py
│           └── auth.py
├── tests/                       # Test files
│   ├── __init__.py
│   ├── conftest.py
│   ├── test_handlers/
│   ├── test_models/
│   └── test_services/
├── migrations/                  # Database migrations
├── docs/                        # Documentation
├── scripts/                     # Utility scripts
├── .env.example                 # Environment variables template
├── .gitignore                   # Git ignore file
├── .pre-commit-config.yaml      # Pre-commit configuration
├── pyproject.toml              # Project configuration
├── requirements.txt            # Production dependencies
├── requirements-dev.txt        # Development dependencies
├── Dockerfile                  # Docker configuration
├── docker-compose.yml          # Docker Compose configuration
└── README.md                   # This file
```

## Quick Start

### 1. Clone the repository

```bash
git clone <repository-url>
cd telegram-bot
```

### 2. Set up virtual environment

```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
pip install -r requirements-dev.txt
```

### 4. Set up environment variables

```bash
cp .env.example .env
# Edit .env with your configuration
```

### 5. Set up database

```bash
# Run database migrations
alembic upgrade head
```

### 6. Run the bot

```bash
python -m src.bot.main
```

## Development

### Code Quality

This project uses several tools to maintain code quality:

- **Black**: Code formatting
- **isort**: Import sorting
- **mypy**: Static type checking
- **flake8**: Linting
- **pytest**: Testing

### Running tests

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=src

# Run specific test file
pytest tests/test_handlers/test_commands.py
```

### Pre-commit hooks

Install pre-commit hooks to automatically run code quality checks:

```bash
pre-commit install
```

### Database migrations

Create a new migration:

```bash
alembic revision --autogenerate -m "Description of changes"
```

Apply migrations:

```bash
alembic upgrade head
```

### Docker

Build and run with Docker:

```bash
docker-compose up --build
```

## Configuration

All configuration is managed through environment variables. See `.env.example` for available options.

### Required Variables

- `BOT_TOKEN`: Your Telegram bot token from @BotFather
- `DATABASE_URL`: Database connection string
- `SECRET_KEY`: Secret key for encryption

### Optional Variables

- `DEBUG`: Enable debug mode (default: False)
- `LOG_LEVEL`: Logging level (default: INFO)
- `REDIS_URL`: Redis connection string for caching
- `SENTRY_DSN`: Sentry DSN for error tracking

## Deployment

### Production checklist

- [ ] Set `DEBUG=False` in production
- [ ] Configure secure database credentials
- [ ] Set up proper logging
- [ ] Configure monitoring (Sentry)
- [ ] Set up SSL certificates for webhooks
- [ ] Configure reverse proxy (nginx)
- [ ] Set up automated backups

### Docker deployment

```bash
docker-compose -f docker-compose.prod.yml up -d
```

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests for new functionality
5. Run the test suite
6. Submit a pull request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Support

For support, please create an issue in the GitHub repository or contact the maintainers.
