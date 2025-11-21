"""
Response caching with TTL for API requests
"""

import hashlib
import json
import time
from typing import Optional, Dict, Any, Callable
from functools import wraps
from collections import OrderedDict

try:
    try:
        from cachetools import TTLCache, LRUCache
    except ImportError:
        TTLCache = None
        LRUCache = None
    CACHETOOLS_AVAILABLE = True
except ImportError:
    CACHETOOLS_AVAILABLE = False

from .logger import get_logger

logger = get_logger("api_wrapper.cache")


class SimpleTTLCache:
    """Simple TTL cache implementation if cachetools not available"""
    
    def __init__(self, maxsize: int = 1000, ttl: int = 3600):
        self.maxsize = maxsize
        self.ttl = ttl
        self.cache: OrderedDict = OrderedDict()
        self.timestamps: Dict[str, float] = {}
    
    def _is_expired(self, key: str) -> bool:
        """Check if cache entry is expired"""
        if key not in self.timestamps:
            return True
        return time.time() - self.timestamps[key] > self.ttl
    
    def _cleanup(self):
        """Remove expired entries"""
        expired_keys = [
            key for key in self.cache.keys()
            if self._is_expired(key)
        ]
        for key in expired_keys:
            del self.cache[key]
            del self.timestamps[key]
    
    def get(self, key: str) -> Optional[Any]:
        """Get value from cache"""
        self._cleanup()
        if key in self.cache and not self._is_expired(key):
            # Move to end (LRU)
            value = self.cache.pop(key)
            self.cache[key] = value
            return value
        return None
    
    def set(self, key: str, value: Any):
        """Set value in cache"""
        self._cleanup()
        if len(self.cache) >= self.maxsize:
            # Remove oldest entry
            self.cache.popitem(last=False)
        self.cache[key] = value
        self.timestamps[key] = time.time()
    
    def clear(self):
        """Clear all cache entries"""
        self.cache.clear()
        self.timestamps.clear()


class ResponseCache:
    """Cache for API responses"""
    
    def __init__(
        self,
        maxsize: int = 1000,
        ttl: int = 3600,
        enabled: bool = True,
    ):
        self.enabled = enabled
        self.maxsize = maxsize
        self.ttl = ttl
        
        if CACHETOOLS_AVAILABLE:
            self.cache = TTLCache(maxsize=maxsize, ttl=ttl)
            logger.info(f"Using cachetools for caching (maxsize={maxsize}, ttl={ttl}s)")
        else:
            self.cache = SimpleTTLCache(maxsize=maxsize, ttl=ttl)
            logger.warning(
                "cachetools not available. Using simple cache implementation. "
                "Install cachetools for better performance."
            )
        
        self.logger = get_logger("api_wrapper.cache")
    
    def _generate_key(
        self,
        provider: str,
        model: str,
        messages: Any,
        **kwargs
    ) -> str:
        """Generate cache key from request parameters"""
        # Create a hash of the request
        key_data = {
            "provider": provider,
            "model": model,
            "messages": messages,
            **kwargs
        }
        key_str = json.dumps(key_data, sort_keys=True)
        return hashlib.sha256(key_str.encode()).hexdigest()
    
    def get(
        self,
        provider: str,
        model: str,
        messages: Any,
        **kwargs
    ) -> Optional[Dict[str, Any]]:
        """
        Get cached response
        
        Args:
            provider: Provider name
            model: Model name
            messages: Request messages
            **kwargs: Additional request parameters
        
        Returns:
            Cached response or None
        """
        if not self.enabled:
            return None
        
        key = self._generate_key(provider, model, messages, **kwargs)
        
        try:
            if CACHETOOLS_AVAILABLE:
                result = self.cache.get(key)
            else:
                result = self.cache.get(key)
            
            if result:
                self.logger.debug(f"Cache hit for {provider}:{model}")
                return result
            
            self.logger.debug(f"Cache miss for {provider}:{model}")
            return None
        except Exception as e:
            self.logger.warning(f"Error retrieving from cache: {e}")
            return None
    
    def set(
        self,
        provider: str,
        model: str,
        messages: Any,
        response: Dict[str, Any],
        **kwargs
    ):
        """
        Cache a response
        
        Args:
            provider: Provider name
            model: Model name
            messages: Request messages
            response: Response to cache
            **kwargs: Additional request parameters
        """
        if not self.enabled:
            return
        
        key = self._generate_key(provider, model, messages, **kwargs)
        
        try:
            if CACHETOOLS_AVAILABLE:
                self.cache[key] = response
            else:
                self.cache.set(key, response)
            
            self.logger.debug(f"Cached response for {provider}:{model}")
        except Exception as e:
            self.logger.warning(f"Error caching response: {e}")
    
    def clear(self):
        """Clear all cached entries"""
        try:
            if CACHETOOLS_AVAILABLE:
                self.cache.clear()
            else:
                self.cache.clear()
            self.logger.info("Cache cleared")
        except Exception as e:
            self.logger.warning(f"Error clearing cache: {e}")
    
    def get_stats(self) -> Dict[str, Any]:
        """Get cache statistics"""
        try:
            if CACHETOOLS_AVAILABLE:
                size = len(self.cache)
            else:
                size = len(self.cache.cache)
            
            return {
                "enabled": self.enabled,
                "maxsize": self.maxsize,
                "ttl": self.ttl,
                "current_size": size,
            }
        except Exception as e:
            self.logger.warning(f"Error getting cache stats: {e}")
            return {"enabled": self.enabled, "error": str(e)}


def cached(
    cache: Optional[ResponseCache] = None,
    ttl: int = 3600,
    enabled: bool = True,
):
    """
    Decorator to cache function results
    
    Args:
        cache: Optional cache instance
        ttl: Time to live in seconds
        enabled: Whether caching is enabled
    """
    def decorator(func: Callable) -> Callable:
        if cache is None:
            _cache = ResponseCache(ttl=ttl, enabled=enabled)
        else:
            _cache = cache
        
        @wraps(func)
        def wrapper(*args, **kwargs):
            # Generate cache key from function arguments
            key_data = {
                "func": func.__name__,
                "args": str(args),
                "kwargs": str(sorted(kwargs.items()))
            }
            key = hashlib.sha256(json.dumps(key_data, sort_keys=True).encode()).hexdigest()
            
            # Try to get from cache
            if _cache.enabled:
                try:
                    if CACHETOOLS_AVAILABLE:
                        cached_result = _cache.cache.get(key)
                    else:
                        cached_result = _cache.cache.get(key)
                    
                    if cached_result is not None:
                        logger.debug(f"Cache hit for {func.__name__}")
                        return cached_result
                except Exception:
                    pass
            
            # Execute function
            result = func(*args, **kwargs)
            
            # Cache result
            if _cache.enabled:
                try:
                    if CACHETOOLS_AVAILABLE:
                        _cache.cache[key] = result
                    else:
                        _cache.cache.set(key, result)
                except Exception:
                    pass
            
            return result
        
        return wrapper
    return decorator


# Global cache instance
_default_cache: Optional[ResponseCache] = None


def get_cache() -> ResponseCache:
    """Get or create default cache instance"""
    global _default_cache
    if _default_cache is None:
        from .settings import get_settings
        settings = get_settings()
        _default_cache = ResponseCache(
            maxsize=settings.cache_max_size,
            ttl=settings.cache_ttl,
            enabled=settings.cache_enabled,
        )
    return _default_cache

