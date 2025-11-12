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

## Docker Deployment

### Dockerfile

```dockerfile
FROM python:3.11-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    g++ \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements
COPY requirements.txt pyproject.toml ./
RUN pip install --no-cache-dir -r requirements.txt
RUN pip install --no-cache-dir -e .

# Copy application code
COPY . .

# Set environment variables
ENV PYTHONUNBUFFERED=1
ENV LOG_LEVEL=INFO
ENV CACHE_ENABLED=true

# Expose health check port
EXPOSE 8080

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD python -c "from api_wrapper.health import get_health_checker; import sys; h = get_health_checker(); status, code = h.get_http_response('liveness'); sys.exit(0 if code == 200 else 1)"

# Run application
CMD ["python", "-m", "api_wrapper"]
```

### Docker Compose

```yaml
version: '3.8'

services:
  chatbot-api:
    build: .
    ports:
      - "8080:8080"
    environment:
      - OPENAI_API_KEY=${OPENAI_API_KEY}
      - HUGGINGFACE_API_KEY=${HUGGINGFACE_API_KEY}
      - LOG_LEVEL=INFO
      - CACHE_ENABLED=true
    volumes:
      - ./logs:/app/logs
    healthcheck:
      test: ["CMD", "python", "-c", "from api_wrapper.health import get_health_checker; h = get_health_checker(); status, code = h.get_http_response('liveness'); exit(0 if code == 200 else 1)"]
      interval: 30s
      timeout: 10s
      retries: 3
    restart: unless-stopped

  prometheus:
    image: prom/prometheus:latest
    ports:
      - "9090:9090"
    volumes:
      - ./prometheus.yml:/etc/prometheus/prometheus.yml
      - prometheus-data:/prometheus
    command:
      - '--config.file=/etc/prometheus/prometheus.yml'

  grafana:
    image: grafana/grafana:latest
    ports:
      - "3000:3000"
    environment:
      - GF_SECURITY_ADMIN_PASSWORD=admin
    volumes:
      - grafana-data:/var/lib/grafana

volumes:
  prometheus-data:
  grafana-data:
```

## Kubernetes Deployment

### Deployment Manifest

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: chatbot-api
  labels:
    app: chatbot-api
spec:
  replicas: 3
  selector:
    matchLabels:
      app: chatbot-api
  template:
    metadata:
      labels:
        app: chatbot-api
    spec:
      containers:
      - name: chatbot-api
        image: your-registry/chatbot-api-wrapper:latest
        ports:
        - containerPort: 8080
        env:
        - name: OPENAI_API_KEY
          valueFrom:
            secretKeyRef:
              name: chatbot-secrets
              key: openai-api-key
        - name: HUGGINGFACE_API_KEY
          valueFrom:
            secretKeyRef:
              name: chatbot-secrets
              key: huggingface-api-key
        livenessProbe:
          httpGet:
            path: /health/liveness
            port: 8080
          initialDelaySeconds: 30
          periodSeconds: 10
        readinessProbe:
          httpGet:
            path: /health/readiness
            port: 8080
          initialDelaySeconds: 5
          periodSeconds: 5
        resources:
          requests:
            memory: "512Mi"
            cpu: "250m"
          limits:
            memory: "1Gi"
            cpu: "500m"
---
apiVersion: v1
kind: Service
metadata:
  name: chatbot-api-service
spec:
  selector:
    app: chatbot-api
  ports:
  - protocol: TCP
    port: 80
    targetPort: 8080
  type: LoadBalancer
---
apiVersion: autoscaling/v2
kind: HorizontalPodAutoscaler
metadata:
  name: chatbot-api-hpa
spec:
  scaleTargetRef:
    apiVersion: apps/v1
    kind: Deployment
    name: chatbot-api
  minReplicas: 3
  maxReplicas: 10
  metrics:
  - type: Resource
    resource:
      name: cpu
      target:
        type: Utilization
        averageUtilization: 70
```

## Monitoring Integration

### Prometheus Configuration

```yaml
# prometheus.yml
global:
  scrape_interval: 15s

scrape_configs:
  - job_name: 'chatbot-api'
    static_configs:
      - targets: ['chatbot-api:8080']
    metrics_path: '/metrics'
```

### Metrics Endpoint Example

```python
from flask import Flask, Response
from api_wrapper.metrics import get_metrics_collector

app = Flask(__name__)

@app.route('/metrics')
def metrics():
    collector = get_metrics_collector()
    prometheus_metrics = collector.export_prometheus()
    return Response(prometheus_metrics, mimetype='text/plain')

@app.route('/health')
def health():
    from api_wrapper.health import get_health_checker
    checker = get_health_checker()
    status, code = checker.get_http_response('health')
    return status, code
```

### Grafana Dashboard

Key metrics to monitor:
- Request rate (requests/second)
- Error rate (errors/second)
- Response time (p50, p95, p99)
- Token usage
- Provider availability
- Cache hit rate

## Logging and Observability

### Structured Logging

```python
from api_wrapper.logger import setup_logger
import structlog

logger = setup_logger(
    name="chatbot_api",
    level="INFO",
    json_format=True,
    sanitize=True,
)

# Use structured logging
logger.info(
    "request_completed",
    extra={
        "model": "gpt-3.5-turbo",
        "provider": "openai",
        "duration_ms": 1234,
        "tokens": 500,
    }
)
```

### Log Aggregation

For production, integrate with:
- **ELK Stack** (Elasticsearch, Logstash, Kibana)
- **Loki** (Grafana Loki)
- **Datadog**
- **New Relic**
- **Splunk**

## Performance Tuning

### Connection Pooling

```python
from api_wrapper.pool import get_connection_pool

pool = get_connection_pool()
pool.configure(maxsize=10, timeout=30)
```

### Caching Strategy

```python
from api_wrapper.cache import get_cache

cache = get_cache()
cache.enabled = True
cache.ttl = 3600  # 1 hour
cache.maxsize = 10000  # Cache up to 10k responses
```

### Rate Limiting

```python
from api_wrapper.rate_limiter import get_rate_limiter

limiter = get_rate_limiter()
limiter.configure(
    provider="openai",
    rate=50.0,  # 50 requests/second
    burst=100.0,
)
```

## Scaling Considerations

1. **Horizontal Scaling**: Deploy multiple instances behind a load balancer
2. **Vertical Scaling**: Increase resources for single instance
3. **Auto-scaling**: Use Kubernetes HPA or cloud auto-scaling
4. **Caching**: Reduce API calls with aggressive caching
5. **Connection Pooling**: Reuse connections efficiently
6. **Async Processing**: Use async clients for concurrent requests
