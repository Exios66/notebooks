# Production Deployment Guide

This guide covers deploying the Chatbot API Wrapper in production environments.

## Pre-Deployment Checklist

- [ ] All dependencies installed and tested
- [ ] Environment variables configured
- [ ] API keys secured and validated
- [ ] Logging configured appropriately
- [ ] Rate limiting configured
- [ ] Error handling tested
- [ ] Monitoring and metrics enabled
- [ ] Health checks implemented
- [ ] Security measures in place
- [ ] Performance tested under load

## Configuration

### Environment Variables

Create a `.env` file or set environment variables:

```bash
# Required
OPENAI_API_KEY=your-key-here
HUGGINGFACE_API_KEY=your-key-here

# Optional - Logging
LOG_LEVEL=INFO
LOG_FILE=/var/log/chatbot-api.log
LOG_JSON=true

# Optional - Rate Limiting
DEFAULT_RATE_LIMIT=10.0
DEFAULT_BURST_LIMIT=20.0

# Optional - Retry Configuration
MAX_RETRIES=3
INITIAL_RETRY_DELAY=1.0
MAX_RETRY_DELAY=60.0

# Optional - Caching
CACHE_ENABLED=true
CACHE_TTL=3600
CACHE_MAX_SIZE=1000
```

### Production Settings

For production, use:

```python
from api_wrapper import ChatbotWrapper
from api_wrapper.settings import get_settings

settings = get_settings()
settings.environment = "production"
settings.log_level = "WARNING"  # Reduce log verbosity
settings.cache_enabled = True
```

## Error Handling

The wrapper includes comprehensive error handling:

```python
from api_wrapper import ChatbotWrapper
from api_wrapper.exceptions import (
    RateLimitError,
    AuthenticationError,
    ModelNotFoundError,
)

wrapper = ChatbotWrapper(openai_api_key="your-key")

try:
    response = wrapper.chat(model="gpt-3.5-turbo", messages="Hello")
except RateLimitError as e:
    # Handle rate limiting
    print(f"Rate limited. Retry after {e.retry_after}s")
except AuthenticationError as e:
    # Handle authentication issues
    print("Authentication failed")
except ModelNotFoundError as e:
    # Handle model not found
    print(f"Model {e.model} not found")
```

## Logging

Configure structured logging:

```python
from api_wrapper.logger import setup_logger

logger = setup_logger(
    name="chatbot_api",
    level="INFO",
    log_file="/var/log/chatbot-api.log",
    json_format=True,  # For log aggregation systems
    sanitize=True,  # Remove sensitive data
)
```

## Rate Limiting

Configure rate limits per provider:

```python
from api_wrapper import get_rate_limiter

rate_limiter = get_rate_limiter()

# Configure OpenAI rate limit
rate_limiter.configure(
    provider="openai",
    rate=10.0,  # 10 requests per second
    burst=20.0,  # Allow bursts up to 20
)

# Configure per-model limits
rate_limiter.configure(
    provider="openai",
    model="gpt-4",
    rate=5.0,  # Lower rate for expensive models
    burst=10.0,
)
```

## Retry Logic

Automatic retry with exponential backoff:

```python
from api_wrapper.retry import exponential_backoff

@exponential_backoff(
    max_retries=3,
    initial_delay=1.0,
    max_delay=60.0,
)
def make_request():
    return wrapper.chat(model="gpt-3.5-turbo", messages="Hello")
```

## Caching

Enable response caching:

```python
from api_wrapper import get_cache

cache = get_cache()
cache.enabled = True
cache.ttl = 3600  # 1 hour

# Cache is automatically used by the wrapper
```

## Monitoring

Track metrics and health:

```python
from api_wrapper import get_metrics_collector, get_health_checker

# Get metrics
metrics = get_metrics_collector()
stats = metrics.get_stats()
print(f"Total requests: {stats['request_counts']}")
print(f"Error rate: {stats['error_counts']}")

# Health checks
health = get_health_checker()
health_status = health.check_health()
print(f"Status: {health_status['status']}")
```

## Security Best Practices

1. **Never commit API keys** - Use environment variables
2. **Use secrets management** - AWS Secrets Manager, HashiCorp Vault, etc.
3. **Enable input validation** - Already built-in
4. **Monitor for anomalies** - Use metrics and logging
5. **Rotate API keys regularly**
6. **Use least privilege** - Limit API key permissions

## Performance Optimization

1. **Enable caching** for repeated queries
2. **Use connection pooling** (automatic)
3. **Configure appropriate rate limits**
4. **Monitor token usage** to control costs
5. **Use async clients** for concurrent requests

## Deployment Options

### Standalone Application

```python
# app.py
from api_wrapper import ChatbotWrapper

wrapper = ChatbotWrapper(
    openai_api_key=os.getenv("OPENAI_API_KEY"),
    huggingface_api_key=os.getenv("HUGGINGFACE_API_KEY"),
)

# Your application code
```

### Web Service (Flask)

```python
from flask import Flask, request, jsonify
from api_wrapper import ChatbotWrapper
from api_wrapper.exceptions import APIError

app = Flask(__name__)
wrapper = ChatbotWrapper(openai_api_key=os.getenv("OPENAI_API_KEY"))

@app.route('/chat', methods=['POST'])
def chat():
    try:
        data = request.json
        response = wrapper.chat(
            model=data['model'],
            messages=data['messages'],
        )
        return jsonify(response)
    except APIError as e:
        return jsonify({"error": str(e)}), 400
```

### Docker Deployment

```dockerfile
FROM python:3.11-slim

WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

ENV LOG_LEVEL=INFO
ENV CACHE_ENABLED=true

CMD ["python", "app.py"]
```

## Troubleshooting

### High Error Rates

- Check API key validity
- Verify rate limits aren't exceeded
- Check network connectivity
- Review logs for specific errors

### Performance Issues

- Enable caching
- Adjust rate limits
- Use connection pooling
- Monitor metrics for bottlenecks

### Memory Issues

- Reduce cache size
- Clear cache periodically
- Monitor local model memory usage

## Monitoring and Alerts

Set up alerts for:

- Error rate > 10%
- Provider availability < 95%
- Response time > 5 seconds
- Rate limit errors
- Authentication failures

## Backup and Recovery

- Backup configuration files
- Document API key rotation process
- Have fallback providers configured
- Test disaster recovery procedures

