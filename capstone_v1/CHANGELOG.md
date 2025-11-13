# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

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
