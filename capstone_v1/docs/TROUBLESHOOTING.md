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

