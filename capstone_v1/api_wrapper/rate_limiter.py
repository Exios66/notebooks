"""
Rate limiting implementation using token bucket algorithm
"""

import time
import threading
from typing import Optional, Dict
from dataclasses import dataclass, field

from .logger import get_logger
from .exceptions import RateLimitError

logger = get_logger("api_wrapper.rate_limiter")


@dataclass
class TokenBucket:
    """Token bucket for rate limiting"""
    capacity: float
    refill_rate: float  # tokens per second
    tokens: float = field(default=0.0)
    last_refill: float = field(default_factory=time.time)
    lock: threading.Lock = field(default_factory=threading.Lock)

    def _refill(self):
        """Refill tokens based on elapsed time"""
        now = time.time()
        elapsed = now - self.last_refill
        self.tokens = min(
            self.capacity,
            self.tokens + (elapsed * self.refill_rate)
        )
        self.last_refill = now

    def acquire(self, tokens: float = 1.0) -> bool:
        """
        Try to acquire tokens from the bucket

        Args:
            tokens: Number of tokens to acquire

        Returns:
            True if tokens were acquired, False otherwise
        """
        with self.lock:
            self._refill()
            if self.tokens >= tokens:
                self.tokens -= tokens
                return True
            return False

    def wait_for_tokens(self, tokens: float = 1.0) -> float:
        """
        Wait until tokens are available and acquire them

        Args:
            tokens: Number of tokens to acquire

        Returns:
            Wait time in seconds
        """
        with self.lock:
            self._refill()
            if self.tokens >= tokens:
                self.tokens -= tokens
                return 0.0

            # Calculate wait time
            needed = tokens - self.tokens
            wait_time = needed / self.refill_rate

            # Refill and acquire
            time.sleep(wait_time)
            self._refill()
            self.tokens -= tokens
            return wait_time


class RateLimiter:
    """
    Rate limiter with per-provider and per-model buckets
    """

    def __init__(
        self,
        default_rate: float = 10.0,  # requests per second
        default_burst: float = 20.0,  # burst capacity
    ):
        self.default_rate = default_rate
        self.default_burst = default_burst
        self.buckets: Dict[str, TokenBucket] = {}
        self.lock = threading.Lock()
        self.logger = get_logger("api_wrapper.rate_limiter")

    def _get_bucket_key(self, provider: str, model: Optional[str] = None) -> str:
        """Generate bucket key for provider/model combination"""
        if model:
            return f"{provider}:{model}"
        return provider

    def _get_or_create_bucket(
        self,
        provider: str,
        model: Optional[str] = None,
        rate: Optional[float] = None,
        burst: Optional[float] = None,
    ) -> TokenBucket:
        """Get or create a token bucket for provider/model"""
        key = self._get_bucket_key(provider, model)

        with self.lock:
            if key not in self.buckets:
                bucket_rate = rate or self.default_rate
                bucket_burst = burst or self.default_burst
                self.buckets[key] = TokenBucket(
                    capacity=bucket_burst,
                    refill_rate=bucket_rate
                )
                self.logger.debug(
                    f"Created rate limiter bucket: {key} (rate={bucket_rate}/s, burst={bucket_burst})"
                )
            return self.buckets[key]

    def configure(
        self,
        provider: str,
        rate: float,
        burst: Optional[float] = None,
        model: Optional[str] = None,
    ):
        """
        Configure rate limit for a provider/model

        Args:
            provider: Provider name
            rate: Requests per second
            burst: Burst capacity (defaults to 2 * rate)
            model: Optional model name for per-model limits
        """
        key = self._get_bucket_key(provider, model)
        burst = burst or (rate * 2)

        with self.lock:
            self.buckets[key] = TokenBucket(
                capacity=burst,
                refill_rate=rate
            )
        self.logger.info(f"Configured rate limit for {key}: {rate}/s, burst={burst}")

    def acquire(
        self,
        provider: str,
        model: Optional[str] = None,
        tokens: float = 1.0,
        wait: bool = False,
        rate: Optional[float] = None,
        burst: Optional[float] = None,
    ) -> bool:
        """
        Acquire tokens from rate limiter

        Args:
            provider: Provider name
            model: Optional model name
            tokens: Number of tokens to acquire
            wait: If True, wait until tokens are available
            rate: Optional custom rate (creates temporary bucket)
            burst: Optional custom burst (creates temporary bucket)

        Returns:
            True if tokens were acquired, False otherwise

        Raises:
            RateLimitError if wait=False and tokens not available
        """
        bucket = self._get_or_create_bucket(provider, model, rate, burst)

        if wait:
            wait_time = bucket.wait_for_tokens(tokens)
            if wait_time > 0:
                self.logger.debug(
                    f"Rate limited: waited {wait_time:.2f}s for {provider}:{model or 'default'}"
                )
            return True
        else:
            acquired = bucket.acquire(tokens)
            if not acquired:
                raise RateLimitError(
                    f"Rate limit exceeded for {provider}:{model or 'default'}",
                    details={
                        "provider": provider,
                        "model": model,
                        "tokens_requested": tokens,
                    }
                )
            return True

    def reset(self, provider: Optional[str] = None, model: Optional[str] = None):
        """
        Reset rate limiter buckets

        Args:
            provider: Optional provider to reset (resets all if None)
            model: Optional model to reset
        """
        with self.lock:
            if provider is None:
                self.buckets.clear()
                self.logger.info("Reset all rate limiter buckets")
            else:
                key = self._get_bucket_key(provider, model)
                if key in self.buckets:
                    del self.buckets[key]
                    self.logger.info(f"Reset rate limiter bucket: {key}")


# Global rate limiter instance
_default_rate_limiter: Optional[RateLimiter] = None


def get_rate_limiter() -> RateLimiter:
    """Get or create the default rate limiter instance"""
    global _default_rate_limiter
    if _default_rate_limiter is None:
        _default_rate_limiter = RateLimiter()
    return _default_rate_limiter
