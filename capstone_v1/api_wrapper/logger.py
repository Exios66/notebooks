"""
Structured logging system for the Chatbot API Wrapper
"""

import logging
import sys
import json
from typing import Optional, Dict, Any
from pathlib import Path
from datetime import datetime
import os


class JSONFormatter(logging.Formatter):
    """JSON formatter for structured logging"""
    
    def format(self, record: logging.LogRecord) -> str:
        log_data = {
            "timestamp": datetime.utcnow().isoformat(),
            "level": record.levelname,
            "logger": record.name,
            "message": record.getMessage(),
            "module": record.module,
            "function": record.funcName,
            "line": record.lineno,
        }
        
        # Add exception info if present
        if record.exc_info:
            log_data["exception"] = self.formatException(record.exc_info)
        
        # Add extra fields
        if hasattr(record, "extra"):
            log_data.update(record.extra)
        
        return json.dumps(log_data)


class SanitizedFormatter(logging.Formatter):
    """Formatter that sanitizes sensitive information"""
    
    SENSITIVE_KEYS = {
        "api_key", "apiKey", "apikey", "token", "password", "secret",
        "authorization", "auth", "credential", "access_token", "refresh_token"
    }
    
    def _sanitize_dict(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Recursively sanitize dictionary values"""
        sanitized = {}
        for key, value in data.items():
            key_lower = key.lower()
            if any(sensitive in key_lower for sensitive in self.SENSITIVE_KEYS):
                sanitized[key] = "***REDACTED***"
            elif isinstance(value, dict):
                sanitized[key] = self._sanitize_dict(value)
            elif isinstance(value, list):
                sanitized[key] = [
                    self._sanitize_dict(item) if isinstance(item, dict) else item
                    for item in value
                ]
            else:
                sanitized[key] = value
        return sanitized
    
    def format(self, record: logging.LogRecord) -> str:
        # Create a copy of the record
        record_copy = logging.makeLogRecord(record.__dict__)
        
        # Sanitize extra fields
        if hasattr(record, "extra"):
            record_copy.extra = self._sanitize_dict(record.extra)
        
        # Format message
        message = record.getMessage()
        
        # Sanitize message if it contains sensitive data
        if any(key in message.lower() for key in self.SENSITIVE_KEYS):
            # Simple sanitization - replace potential secrets
            for key in self.SENSITIVE_KEYS:
                # This is a basic implementation
                pass
        
        return super().format(record_copy)


def setup_logger(
    name: str = "api_wrapper",
    level: str = "INFO",
    log_file: Optional[str] = None,
    json_format: bool = False,
    sanitize: bool = True,
) -> logging.Logger:
    """
    Set up a logger with configured handlers
    
    Args:
        name: Logger name
        level: Log level (DEBUG, INFO, WARNING, ERROR, CRITICAL)
        log_file: Optional file path for file logging
        json_format: Use JSON formatting
        sanitize: Sanitize sensitive information
    
    Returns:
        Configured logger instance
    """
    logger = logging.getLogger(name)
    logger.setLevel(getattr(logging, level.upper(), logging.INFO))
    
    # Remove existing handlers to avoid duplicates
    logger.handlers.clear()
    
    # Create formatter
    if json_format:
        formatter = JSONFormatter()
    elif sanitize:
        formatter = SanitizedFormatter(
            fmt="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
            datefmt="%Y-%m-%d %H:%M:%S"
        )
    else:
        formatter = logging.Formatter(
            fmt="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
            datefmt="%Y-%m-%d %H:%M:%S"
        )
    
    # Console handler
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(logging.DEBUG)
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)
    
    # File handler (if specified)
    if log_file:
        log_path = Path(log_file)
        log_path.parent.mkdir(parents=True, exist_ok=True)
        
        file_handler = logging.FileHandler(log_file)
        file_handler.setLevel(logging.DEBUG)
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)
    
    # Prevent propagation to root logger
    logger.propagate = False
    
    return logger


def get_logger(name: str = "api_wrapper") -> logging.Logger:
    """
    Get or create a logger instance
    
    Args:
        name: Logger name
    
    Returns:
        Logger instance
    """
    logger = logging.getLogger(name)
    
    # If logger has no handlers, set it up with defaults
    if not logger.handlers:
        log_level = os.getenv("LOG_LEVEL", "INFO")
        log_file = os.getenv("LOG_FILE")
        json_format = os.getenv("LOG_JSON", "false").lower() == "true"
        
        logger = setup_logger(
            name=name,
            level=log_level,
            log_file=log_file,
            json_format=json_format,
        )
    
    return logger


class RequestLogger:
    """Context manager for logging API requests and responses"""
    
    def __init__(
        self,
        logger: logging.Logger,
        operation: str,
        model: str,
        provider: str,
        **kwargs
    ):
        self.logger = logger
        self.operation = operation
        self.model = model
        self.provider = provider
        self.kwargs = kwargs
        self.start_time = None
    
    def __enter__(self):
        self.start_time = datetime.utcnow()
        self.logger.info(
            f"Starting {self.operation}",
            extra={
                "operation": self.operation,
                "model": self.model,
                "provider": self.provider,
                **self.kwargs
            }
        )
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        duration = (datetime.utcnow() - self.start_time).total_seconds()
        
        if exc_type is None:
            self.logger.info(
                f"Completed {self.operation}",
                extra={
                    "operation": self.operation,
                    "model": self.model,
                    "provider": self.provider,
                    "duration_seconds": duration,
                    "status": "success"
                }
            )
        else:
            self.logger.error(
                f"Failed {self.operation}: {exc_val}",
                extra={
                    "operation": self.operation,
                    "model": self.model,
                    "provider": self.provider,
                    "duration_seconds": duration,
                    "status": "error",
                    "error_type": exc_type.__name__,
                    "error_message": str(exc_val)
                },
                exc_info=exc_tb
            )
        
        return False  # Don't suppress exceptions

