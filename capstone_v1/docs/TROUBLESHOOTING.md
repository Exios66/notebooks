# Troubleshooting Guide

Common issues and solutions for the Chatbot API Wrapper.

## Authentication Errors

### Issue: "Authentication failed"

**Solutions:**

1. Verify API key is correct
2. Check environment variable is set: `echo $OPENAI_API_KEY`
3. Ensure API key hasn't expired
4. Verify API key has required permissions

### Issue: "API key is required"

**Solutions:**

1. Set environment variable: `export OPENAI_API_KEY="your-key"`
2. Pass key directly: `ChatbotWrapper(openai_api_key="your-key")`
3. Check `.env` file is loaded (if using python-dotenv)

## Rate Limiting

### Issue: "Rate limit exceeded"

**Solutions:**

1. Implement retry logic with exponential backoff
2. Reduce request frequency
3. Use rate limiter: `get_rate_limiter().configure(...)`
4. Check provider-specific rate limits
5. Upgrade API tier if available

## Network Errors

### Issue: "Network error" or "Connection timeout"

**Solutions:**

1. Check internet connectivity
2. Verify firewall settings
3. Check proxy configuration if behind corporate firewall
4. Increase timeout: `REQUEST_TIMEOUT=180`
5. Use connection pooling (automatic)

## Model Not Found

### Issue: "Model not found"

**Solutions:**

1. Verify model name is correct
2. Check model is available in your region/tier
3. Ensure you have access to the model
4. Try alternative model name

## Performance Issues

### Issue: Slow responses

**Solutions:**

1. Enable caching: `cache.enabled = True`
2. Use connection pooling (automatic)
3. Reduce max_tokens if not needed
4. Use faster models (e.g., gpt-3.5-turbo vs gpt-4)
5. Check network latency

### Issue: High memory usage

**Solutions:**

1. Reduce cache size: `cache.maxsize = 500`
2. Clear cache periodically: `cache.clear()`
3. Avoid loading large local models
4. Use API instead of local models

## Logging Issues

### Issue: No logs appearing

**Solutions:**

1. Check log level: `LOG_LEVEL=DEBUG`
2. Verify log file path is writable
3. Check logger configuration
4. Ensure logging is initialized

### Issue: Too many logs

**Solutions:**

1. Increase log level: `LOG_LEVEL=WARNING`
2. Disable debug logging
3. Use log rotation
4. Filter logs by level

## Configuration Issues

### Issue: Settings not loading

**Solutions:**

1. Check `.env` file exists and is readable
2. Verify environment variable names
3. Use `python-dotenv` to load `.env`
4. Check for typos in variable names

## Import Errors

### Issue: "Module not found"

**Solutions:**

1. Install dependencies: `pip install -r requirements.txt`
2. Check Python version (requires 3.8+)
3. Verify virtual environment is activated
4. Reinstall package: `pip install -e .`

## Testing Issues

### Issue: Tests failing

**Solutions:**

1. Install test dependencies: `pip install pytest pytest-cov`
2. Check API keys are set (for integration tests)
3. Run with verbose: `pytest -v`
4. Check test markers: `pytest -m "not requires_api"`

## Getting Help

1. Check documentation: `docs/`
2. Review examples: `api_wrapper/examples.py`
3. Check GitHub issues
4. Enable debug logging for more details
5. Review error messages and stack traces

## Common Error Messages

| Error | Cause | Solution |
|-------|-------|----------|
| `AuthenticationError` | Invalid API key | Verify and update API key |
| `RateLimitError` | Too many requests | Implement rate limiting |
| `ModelNotFoundError` | Invalid model name | Check model name |
| `NetworkError` | Connection issue | Check network/proxy |
| `TimeoutError` | Request too slow | Increase timeout |
| `ValidationError` | Invalid input | Check input format |

## Metrics and Health Check Issues

### Issue: Health check failing

**Symptoms:**

- Health endpoint returns 503
- High error rates reported
- Provider availability low

**Solutions:**

1. **Check Metrics**:

   ```python
   from api_wrapper.metrics import get_metrics_collector
   metrics = get_metrics_collector()
   stats = metrics.get_stats()
   print(stats)
   ```

2. **Check Health Status**:

   ```python
   from api_wrapper.health import get_health_checker
   checker = get_health_checker()
   health = checker.check_health()
   print(health)
   ```

3. **Check Dependencies**:

   ```python
   deps = checker.check_dependencies()
   if not deps["all_required_available"]:
       print(f"Missing: {deps['missing_required']}")
   ```

### Issue: Metrics not collecting

**Solutions:**

1. Ensure metrics collector is initialized
2. Check if requests are being tracked
3. Verify metrics context manager is used:

   ```python
   from api_wrapper.metrics import MetricsContext, get_metrics_collector
   
   collector = get_metrics_collector()
   with MetricsContext(collector, "openai", "gpt-3.5-turbo") as ctx:
       # Your API call
       ctx.set_tokens(100)
   ```

### Issue: Prometheus metrics format incorrect

**Solutions:**

1. Verify export format:

   ```python
   prometheus_output = collector.export_prometheus()
   print(prometheus_output)
   ```

2. Check metric names follow Prometheus conventions
3. Ensure labels are properly formatted

## CI/CD Issues

### Issue: Tests failing in CI

**Solutions:**

1. **Check Python Version**: Ensure CI uses correct Python version
2. **Install Dependencies**: Verify all dependencies are installed
3. **Check Environment Variables**: Ensure test API keys are set
4. **Review Test Markers**: Use `pytest -m "not requires_api"` for unit tests

### Issue: Linting failures

**Solutions:**

1. **Run Black**: `black api_wrapper/ tests/`
2. **Fix Flake8**: `flake8 api_wrapper/ tests/ --max-line-length=100`
3. **Type Checking**: `mypy api_wrapper/ --ignore-missing-imports`

### Issue: Security scan failures

**Solutions:**

1. **Update Dependencies**: `pip install --upgrade <package>`
2. **Review Vulnerabilities**: Check Safety/Bandit reports
3. **Fix Security Issues**: Address high/critical vulnerabilities

## Deployment Issues

### Issue: Docker build failing

**Solutions:**

1. Check Dockerfile syntax
2. Verify base image exists
3. Check build context includes all files
4. Review build logs for specific errors

### Issue: Kubernetes pod not starting

**Solutions:**

1. **Check Pod Logs**: `kubectl logs <pod-name>`
2. **Check Events**: `kubectl describe pod <pod-name>`
3. **Verify Secrets**: Ensure API keys are in secrets
4. **Check Resource Limits**: Verify sufficient resources

### Issue: Health checks failing in Kubernetes

**Solutions:**

1. Verify health endpoint is accessible
2. Check liveness/readiness probe configuration
3. Ensure port is correct
4. Review initial delay and timeout settings

## Performance Troubleshooting

### Issue: Slow response times

**Diagnosis:**

1. Check metrics for average durations
2. Identify slow providers/models
3. Review network latency
4. Check cache hit rates

**Solutions:**

1. Enable caching
2. Use faster models
3. Optimize network configuration
4. Implement connection pooling
5. Use async clients for concurrent requests

### Issue: Excessive memory usage

**Diagnosis:**

1. Monitor memory metrics
2. Check cache size
3. Review local model usage

**Solutions:**

1. Reduce cache size
2. Clear cache periodically
3. Use API instead of local models
4. Increase memory limits
5. Implement memory-efficient caching

### Issue: High token usage

**Solutions:**

1. Monitor token metrics:

   ```python
   stats = metrics.get_stats()
   print(stats["total_tokens"])
   ```

2. Optimize prompts to reduce tokens
3. Set lower max_tokens
4. Use caching for repeated queries
5. Monitor costs per provider

## Integration Issues

### Issue: Import errors

**Solutions:**

1. **Install Package**: `pip install -e .`
2. **Check Python Path**: Verify package is in PYTHONPATH
3. **Virtual Environment**: Ensure venv is activated
4. **Dependencies**: Install all required dependencies

### Issue: API wrapper not working with Flask/FastAPI

**Solutions:**

1. Initialize wrapper at app startup
2. Use connection pooling
3. Handle exceptions properly
4. Configure logging appropriately

### Issue: Metrics not appearing in Prometheus

**Solutions:**

1. Verify metrics endpoint is accessible
2. Check Prometheus scrape configuration
3. Ensure metrics format is correct
4. Check network connectivity

## Debugging Tips

1. **Enable Debug Logging**:

   ```python
   import logging
   logging.basicConfig(level=logging.DEBUG)
   ```

2. **Use Metrics Context**:

   ```python
   with MetricsContext(collector, provider, model) as ctx:
       # Track your request
   ```

3. **Check Health Status**:

   ```python
   health = checker.check_health()
   if health["status"] != "healthy":
       print(f"Issues: {health['issues']}")
   ```

4. **Export Metrics**:

   ```python
   # Prometheus format
   print(collector.export_prometheus())
   
   # JSON format
   print(collector.export_json())
   ```

5. **Monitor in Real-time**:

   ```python
   import time
   while True:
       stats = metrics.get_stats()
       print(f"Requests: {sum(stats['request_counts'].values())}")
       print(f"Errors: {sum(stats['error_counts'].values())}")
       time.sleep(5)
   ```
