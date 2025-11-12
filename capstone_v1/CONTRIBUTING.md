# Contributing Guide

Thank you for your interest in contributing to the Chatbot API Wrapper!

## Getting Started

1. Fork the repository
2. Clone your fork: `git clone https://github.com/yourusername/notebooks.git`
3. Create a branch: `git checkout -b feature/your-feature-name`
4. Make your changes
5. Test your changes
6. Commit: `git commit -m "Add your feature"`
7. Push: `git push origin feature/your-feature-name`
8. Open a Pull Request

## Development Setup

```bash
# Install dependencies
pip install -r requirements.txt

# Install development dependencies
pip install -r requirements.txt[dev]

# Run tests
pytest tests/

# Run with coverage
pytest tests/ --cov=api_wrapper --cov-report=html
```

## Code Style

We use:
- **Black** for code formatting
- **Flake8** for linting
- **MyPy** for type checking

```bash
# Format code
black api_wrapper/ tests/

# Lint
flake8 api_wrapper/ tests/

# Type check
mypy api_wrapper/
```

## Testing

- Write tests for new features
- Ensure all tests pass: `pytest`
- Aim for >80% code coverage
- Add integration tests for complex features

## Documentation

- Update docstrings for new functions/classes
- Add examples to documentation
- Update README if needed
- Keep CHANGELOG.md updated

## Pull Request Process

1. Ensure tests pass
2. Update documentation
3. Add changelog entry
4. Request review
5. Address feedback
6. Squash commits if requested

## Code of Conduct

- Be respectful
- Welcome newcomers
- Focus on constructive feedback
- Help others learn

## Questions?

Open an issue or contact the maintainers.

