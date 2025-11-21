# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.1.0] - 2024-12-XX

### Added

- **Comprehensive Models Registry** (`models/models_registry.py`)
  - Complete information for 17 publicly sourceable models (10 HuggingFace, 7 OpenAI)
  - Full API endpoints with URLs, methods, and rate limits
  - Model specifications (parameters, context windows, architecture)
  - Licensing information and URLs
  - Cost information and free tier availability
  - Recommended use cases and limitations
  - Documentation and model card links
  - Supported languages and default parameters
  - JSON export functionality for programmatic access

- **Models Registry CLI Script** (`scripts/list-models.py`)
  - List all models or filter by provider
  - Search models by query
  - Show detailed model information
  - List free tier models
  - List models that can run locally
  - Export registry to JSON

- **Enhanced ChatbotWrapper Integration**
  - `get_model_info()` now uses models registry when available
  - `list_models()` integrates with models registry
  - Automatic fallback to basic config if registry unavailable
  - Comprehensive model information returned as dictionaries

- **New Examples** (6 new examples in `examples.py`)
  - Models registry information retrieval
  - Model search functionality
  - Free tier model discovery
  - Local model identification
  - Model comparison by provider and type
  - Integration with ChatbotWrapper

- **Comprehensive Tests** (`tests/test_models_registry.py`)
  - Full test coverage for models registry functionality
  - Tests for model information retrieval
  - Tests for search and filtering functions
  - Tests for export functionality

- **Updated Documentation**
  - Models registry section in API reference
  - Usage examples and CLI documentation
  - Integration guide with ChatbotWrapper

### Changed

- `ChatbotWrapper.get_model_info()` now returns comprehensive information from models registry
- `ChatbotWrapper.list_models()` uses models registry for complete model lists
- Enhanced model information includes specs, endpoints, and use cases

### Documentation

- Added `models/README.md` with comprehensive registry documentation
- Updated `docs/api-reference.md` with models registry information
- Added example usage script (`models/example_usage.py`)

## [1.0.0] - 2024-11-12

### Added

- Integrated Prometheus-compatible metrics collection and export
- Added provider and model statistics (requests, errors, tokens, response lengths)
- Implemented health check endpoints with dependency checks
- Enhanced documentation for production, security, and troubleshooting
- Improved CI/CD with security scans (Safety, Bandit), coverage reports, and publishing workflow
- Provided deployment and monitoring examples (Docker, Kubernetes, Prometheus/Grafana)
- Added example scripts for metrics and health checks

- Initial release of Chatbot API Wrapper
- Support for OpenAI and HuggingFace models
- Unified interface for multiple providers
- Streaming responses
- Conversation management
- Starter prompts for various domains
- Dataset loaders for fine-tuning
- Comprehensive error handling and logging
- Retry logic with exponential backoff
- Rate limiting with token bucket algorithm
- Response caching with TTL
- Connection pooling
- Input validation and security
- Metrics collection and health checks
- Production-ready configuration management
- Comprehensive test suite
- Complete documentation

### Security

- Input validation and sanitization
- API key masking in logs
- Secure credential handling
- Request size limits

### Performance

- Response caching
- Connection pooling
- Efficient streaming
- Memory optimization
