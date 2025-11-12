# Security Best Practices

This document outlines security best practices for using the Chatbot API Wrapper in production.

## API Key Management

### Never Commit API Keys

**Bad:**

```python
# Never do this!
wrapper = ChatbotWrapper(openai_api_key="sk-1234567890abcdef")
```

**Good:**

```python
import os
wrapper = ChatbotWrapper(openai_api_key=os.getenv("OPENAI_API_KEY"))
```

### Use Environment Variables

```bash
export OPENAI_API_KEY="sk-..."
export HUGGINGFACE_API_KEY="hf_..."
```

### Secrets Management

For production, use proper secrets management:

- **AWS Secrets Manager**
- **HashiCorp Vault**
- **Azure Key Vault**
- **Google Secret Manager**

## Input Validation

The wrapper includes built-in input validation:

```python
from api_wrapper.security import validate_messages, validate_model_name

# Validate messages
messages = validate_messages(user_input)

# Validate model name
model = validate_model_name(user_model)
```

### Security Features

- Maximum message length: 100,000 characters
- Maximum messages: 100 per request
- Model name validation
- Parameter range validation
- Automatic sanitization in logs

## Logging Security

Sensitive data is automatically sanitized in logs:

```python
from api_wrapper.logger import setup_logger

logger = setup_logger(sanitize=True)  # Enabled by default
```

The logger automatically redacts:

- API keys
- Tokens
- Passwords
- Secrets
- Credentials

## Rate Limiting

Prevent abuse with rate limiting:

```python
from api_wrapper import get_rate_limiter

rate_limiter = get_rate_limiter()
rate_limiter.configure(
    provider="openai",
    rate=10.0,  # Limit to 10 requests/second
    burst=20.0,
)
```

## Error Handling

Don't expose sensitive information in error messages:

```python
from api_wrapper.exceptions import APIError

try:
    response = wrapper.chat(...)
except APIError as e:
    # Log full error internally
    logger.error(f"API error: {e}", exc_info=True)
    
    # Return generic message to user
    return {"error": "Request failed. Please try again."}
```

## Network Security

- Use HTTPS for all API communications
- Verify SSL certificates
- Use VPN or private networks when possible
- Monitor for suspicious network activity

## Access Control

- Implement authentication for your application
- Use API keys with minimal required permissions
- Rotate keys regularly
- Monitor API usage for anomalies

## Content Security

- Validate and sanitize user inputs
- Filter sensitive data from responses
- Implement content filtering if needed
- Monitor for injection attempts

## Compliance

### Data Privacy

- Don't log user messages without consent
- Implement data retention policies
- Comply with GDPR, CCPA, etc.
- Encrypt sensitive data at rest

### Audit Logging

```python
from api_wrapper.logger import get_logger

logger = get_logger("audit")
logger.info(
    "API request",
    extra={
        "user_id": user_id,
        "model": model,
        "timestamp": datetime.utcnow().isoformat(),
    }
)
```

## Security Checklist

- [ ] API keys stored securely (not in code)
- [ ] Environment variables used for configuration
- [ ] Input validation enabled
- [ ] Logging sanitization enabled
- [ ] Rate limiting configured
- [ ] Error messages don't expose sensitive data
- [ ] HTTPS used for all communications
- [ ] Access control implemented
- [ ] Security monitoring enabled
- [ ] Regular security audits performed

## Reporting Security Issues

If you discover a security vulnerability:

1. **Do not** open a public issue
2. Email <security@yourdomain.com>
3. Include details and steps to reproduce
4. Allow time for fix before disclosure

## Vulnerability Scanning

### Automated Scanning

Use tools to scan for vulnerabilities:

```bash
# Safety - Check for known vulnerabilities
pip install safety
safety check

# Bandit - Security linter
pip install bandit
bandit -r api_wrapper/

# Snyk
snyk test

# OWASP Dependency Check
dependency-check --scan api_wrapper/
```

### CI/CD Integration

Add security scanning to your CI/CD pipeline:

```yaml
# .github/workflows/security.yml
- name: Run Safety check
  run: safety check

- name: Run Bandit
  run: bandit -r api_wrapper/ -ll

- name: Run Snyk
  run: snyk test --severity-threshold=high
```

### Dependency Updates

Regularly update dependencies:

```bash
# Check for outdated packages
pip list --outdated

# Update with pip-tools
pip-compile --upgrade requirements.txt
```

## Compliance

### GDPR Compliance

- **Data Minimization**: Only collect necessary data
- **Right to Erasure**: Implement data deletion
- **Data Portability**: Export user data
- **Privacy by Design**: Default privacy settings

### SOC 2 Compliance

- **Access Controls**: Implement authentication/authorization
- **Audit Logging**: Log all access and changes
- **Encryption**: Encrypt data at rest and in transit
- **Monitoring**: Continuous security monitoring

### HIPAA Compliance (if applicable)

- **Encryption**: Encrypt PHI data
- **Access Controls**: Strict access management
- **Audit Logs**: Comprehensive logging
- **Business Associate Agreements**: With third-party providers

## Security Incident Response

### Incident Response Plan

1. **Detection**: Monitor for security events
2. **Containment**: Isolate affected systems
3. **Eradication**: Remove threats
4. **Recovery**: Restore normal operations
5. **Lessons Learned**: Post-incident review

### Security Monitoring

Monitor for:

- Unusual API usage patterns
- Authentication failures
- Rate limit violations
- Unauthorized access attempts
- Data exfiltration attempts

### Security Alerts

Set up alerts for:

- Multiple failed authentication attempts
- Unusual token usage
- API key exposure
- High error rates
- Suspicious network activity

## Secure Development Practices

### Code Review

- Review all code changes
- Check for security vulnerabilities
- Verify input validation
- Ensure proper error handling

### Security Testing

- **Static Analysis**: Use tools like Bandit, SonarQube
- **Dynamic Analysis**: Penetration testing
- **Dependency Scanning**: Check for vulnerable dependencies
- **Fuzzing**: Test with malformed inputs

### Threat Modeling

Identify and mitigate threats:

1. **Spoofing**: Authentication mechanisms
2. **Tampering**: Input validation, integrity checks
3. **Repudiation**: Audit logging
4. **Information Disclosure**: Encryption, access controls
5. **Denial of Service**: Rate limiting, resource limits
6. **Elevation of Privilege**: Authorization checks

## Security Tools

### Recommended Tools

- **Safety**: Dependency vulnerability scanning
- **Bandit**: Security linter for Python
- **Snyk**: Vulnerability management
- **OWASP ZAP**: Security testing
- **TruffleHog**: Secret scanning
- **GitGuardian**: Secret detection in Git

### Integration Example

```python
# pre-commit hook for security
# .pre-commit-config.yaml
repos:
  - repo: https://github.com/PyCQA/bandit
    rev: 1.7.5
    hooks:
      - id: bandit
        args: ["-r", "api_wrapper/"]
  
  - repo: https://github.com/pyupio/safety
    rev: 2.3.5
    hooks:
      - id: safety
        args: ["--json"]
```

## Additional Resources

- [OWASP Top 10](https://owasp.org/www-project-top-ten/)
- [Python Security Best Practices](https://python.readthedocs.io/en/stable/library/security.html)
- [API Security Best Practices](https://owasp.org/www-project-api-security/)
- [CWE Top 25](https://cwe.mitre.org/top25/)
- [NIST Cybersecurity Framework](https://www.nist.gov/cyberframework)
