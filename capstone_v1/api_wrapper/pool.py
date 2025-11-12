"""
Connection pooling for HTTP clients
"""

import requests
from typing import Optional
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

from .logger import get_logger

logger = get_logger("api_wrapper.pool")


class ConnectionPool:
    """
    Connection pool manager for HTTP requests
    """
    
    def __init__(
        self,
        pool_connections: int = 10,
        pool_maxsize: int = 10,
        max_retries: int = 3,
        backoff_factor: float = 0.3,
    ):
        """
        Initialize connection pool
        
        Args:
            pool_connections: Number of connection pools to cache
            pool_maxsize: Maximum number of connections to save in the pool
            max_retries: Maximum number of retries
            backoff_factor: Backoff factor for retries
        """
        self.pool_connections = pool_connections
        self.pool_maxsize = pool_maxsize
        self.max_retries = max_retries
        self.backoff_factor = backoff_factor
        
        # Create retry strategy
        retry_strategy = Retry(
            total=max_retries,
            backoff_factor=backoff_factor,
            status_forcelist=[429, 500, 502, 503, 504],
            allowed_methods=["POST", "GET"]
        )
        
        # Create adapter with connection pooling
        self.adapter = HTTPAdapter(
            pool_connections=pool_connections,
            pool_maxsize=pool_maxsize,
            max_retries=retry_strategy
        )
        
        self.logger = get_logger("api_wrapper.connection_pool")
        self.logger.info(
            f"Connection pool initialized (connections={pool_connections}, "
            f"maxsize={pool_maxsize}, retries={max_retries})"
        )
    
    def get_session(self, base_url: Optional[str] = None) -> requests.Session:
        """
        Get a session with connection pooling configured
        
        Args:
            base_url: Optional base URL for the session
        
        Returns:
            Configured requests.Session
        """
        session = requests.Session()
        
        if base_url:
            session.mount(base_url, self.adapter)
        else:
            # Mount for all HTTP/HTTPS
            session.mount("http://", self.adapter)
            session.mount("https://", self.adapter)
        
        return session


# Global connection pool instance
_default_pool: Optional[ConnectionPool] = None


def get_connection_pool() -> ConnectionPool:
    """Get or create default connection pool"""
    global _default_pool
    if _default_pool is None:
        _default_pool = ConnectionPool()
    return _default_pool

