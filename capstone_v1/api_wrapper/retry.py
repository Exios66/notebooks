"""
Retry logic with exponential backoff for API requests
"""

import time
import random
from typing import Callable, TypeVar, Optional, Type, Tuple
from functools import wraps
import logging

from .exceptions import RateLimitError, TimeoutError, NetworkError, APIError
from .logger import get_logger

T = TypeVar('T')
logger = get_logger("api_wrapper.retry")


def exponential_backoff(
    max_retries: int = 3,
    initial_delay: float = 1.0,
    max_delay: float = 60.0,
    exponential_base: float = 2.0,
    jitter: bool = True,
    retryable_exceptions: Tuple[Type[Exception], ...] = (
        RateLimitError,
        TimeoutError,
        NetworkError,
        APIError,
    ),
):
    """
    Decorator for retrying functions with exponential backoff
    
    Args:
        max_retries: Maximum number of retry attempts
        initial_delay: Initial delay in seconds
        max_delay: Maximum delay in seconds
        exponential_base: Base for exponential backoff
        jitter: Add random jitter to delays
        retryable_exceptions: Tuple of exceptions that should trigger retry
    
    Returns:
        Decorated function with retry logic
    """
    def decorator(func: Callable[..., T]) -> Callable[..., T]:
        @wraps(func)
        def wrapper(*args, **kwargs) -> T:
            last_exception = None
            
            for attempt in range(max_retries + 1):
                try:
                    return func(*args, **kwargs)
                except retryable_exceptions as e:
                    last_exception = e
                    
                    # Don't retry on last attempt
                    if attempt >= max_retries:
                        logger.error(
                            f"Max retries ({max_retries}) exceeded for {func.__name__}",
                            extra={"attempt": attempt + 1, "error": str(e)}
                        )
                        raise
                    
                    # Calculate delay with exponential backoff
                    delay = min(
                        initial_delay * (exponential_base ** attempt),
                        max_delay
                    )
                    
                    # Add jitter if enabled
                    if jitter:
                        jitter_amount = delay * 0.1 * random.random()
                        delay = delay + jitter_amount
                    
                    # Handle rate limit retry-after
                    if isinstance(e, RateLimitError) and e.retry_after:
                        delay = max(delay, e.retry_after)
                    
                    logger.warning(
                        f"Retrying {func.__name__} after {delay:.2f}s (attempt {attempt + 1}/{max_retries})",
                        extra={
                            "attempt": attempt + 1,
                            "max_retries": max_retries,
                            "delay": delay,
                            "error": str(e)
                        }
                    )
                    
                    time.sleep(delay)
                except Exception as e:
                    # Non-retryable exception, raise immediately
                    logger.error(
                        f"Non-retryable error in {func.__name__}: {e}",
                        exc_info=True
                    )
                    raise
            
            # Should never reach here, but just in case
            if last_exception:
                raise last_exception
            raise RuntimeError(f"Unexpected error in retry wrapper for {func.__name__}")
        
        return wrapper
    return decorator


class RetryHandler:
    """
    Retry handler with configurable strategies
    """
    
    def __init__(
        self,
        max_retries: int = 3,
        initial_delay: float = 1.0,
        max_delay: float = 60.0,
        exponential_base: float = 2.0,
        jitter: bool = True,
    ):
        self.max_retries = max_retries
        self.initial_delay = initial_delay
        self.max_delay = max_delay
        self.exponential_base = exponential_base
        self.jitter = jitter
        self.logger = get_logger("api_wrapper.retry_handler")
    
    def execute(
        self,
        func: Callable[..., T],
        *args,
        retryable_exceptions: Tuple[Type[Exception], ...] = (
            RateLimitError,
            TimeoutError,
            NetworkError,
            APIError,
        ),
        **kwargs
    ) -> T:
        """
        Execute a function with retry logic
        
        Args:
            func: Function to execute
            *args: Positional arguments for func
            retryable_exceptions: Exceptions that should trigger retry
            **kwargs: Keyword arguments for func
        
        Returns:
            Result of func execution
        
        Raises:
            Last exception if all retries fail
        """
        last_exception = None
        
        for attempt in range(self.max_retries + 1):
            try:
                return func(*args, **kwargs)
            except retryable_exceptions as e:
                last_exception = e
                
                if attempt >= self.max_retries:
                    self.logger.error(
                        f"Max retries ({self.max_retries}) exceeded",
                        extra={"attempt": attempt + 1, "error": str(e)}
                    )
                    raise
                
                # Calculate delay
                delay = min(
                    self.initial_delay * (self.exponential_base ** attempt),
                    self.max_delay
                )
                
                if self.jitter:
                    jitter_amount = delay * 0.1 * random.random()
                    delay = delay + jitter_amount
                
                if isinstance(e, RateLimitError) and e.retry_after:
                    delay = max(delay, e.retry_after)
                
                self.logger.warning(
                    f"Retrying after {delay:.2f}s (attempt {attempt + 1}/{self.max_retries})",
                    extra={
                        "attempt": attempt + 1,
                        "delay": delay,
                        "error": str(e)
                    }
                )
                
                time.sleep(delay)
            except Exception as e:
                self.logger.error(f"Non-retryable error: {e}", exc_info=True)
                raise
        
        if last_exception:
            raise last_exception
        raise RuntimeError("Unexpected error in retry handler")

