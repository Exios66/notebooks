"""
Metrics collection for monitoring API usage and performance
"""

import time
from typing import Dict, Any, Optional
from collections import defaultdict
from dataclasses import dataclass, field
from datetime import datetime
import threading

from .logger import get_logger

logger = get_logger("api_wrapper.metrics")


@dataclass
class RequestMetrics:
    """Metrics for a single request"""
    provider: str
    model: str
    start_time: float
    end_time: Optional[float] = None
    success: bool = False
    error_type: Optional[str] = None
    tokens_used: Optional[int] = None
    response_length: Optional[int] = None
    
    @property
    def duration(self) -> Optional[float]:
        """Request duration in seconds"""
        if self.end_time:
            return self.end_time - self.start_time
        return None


class MetricsCollector:
    """Collector for API metrics"""
    
    def __init__(self):
        self.metrics: list = []
        self.lock = threading.Lock()
        self.logger = get_logger("api_wrapper.metrics")
        
        # Aggregated stats
        self.request_count = defaultdict(int)
        self.error_count = defaultdict(int)
        self.total_tokens = defaultdict(int)
        self.total_duration = defaultdict(float)
        self.provider_availability = defaultdict(lambda: {"success": 0, "total": 0})
    
    def record_request(
        self,
        provider: str,
        model: str,
        duration: float,
        success: bool = True,
        error_type: Optional[str] = None,
        tokens_used: Optional[int] = None,
        response_length: Optional[int] = None,
    ):
        """
        Record a request metric
        
        Args:
            provider: Provider name
            model: Model name
            duration: Request duration in seconds
            success: Whether request was successful
            error_type: Error type if failed
            tokens_used: Number of tokens used
            response_length: Response length in characters
        """
        with self.lock:
            key = f"{provider}:{model}"
            self.request_count[key] += 1
            self.total_duration[key] += duration
            
            if tokens_used:
                self.total_tokens[key] += tokens_used
            
            # Update provider availability
            self.provider_availability[provider]["total"] += 1
            if success:
                self.provider_availability[provider]["success"] += 1
            else:
                self.error_count[key] += 1
                if error_type:
                    self.error_count[f"{key}:{error_type}"] += 1
    
    def get_stats(self) -> Dict[str, Any]:
        """
        Get aggregated statistics
        
        Returns:
            Dictionary with statistics
        """
        with self.lock:
            stats = {
                "request_counts": dict(self.request_count),
                "error_counts": dict(self.error_count),
                "total_tokens": dict(self.total_tokens),
                "provider_availability": {},
            }
            
            # Calculate availability percentages
            for provider, counts in self.provider_availability.items():
                total = counts["total"]
                success = counts["success"]
                stats["provider_availability"][provider] = {
                    "total_requests": total,
                    "successful_requests": success,
                    "availability_percent": (success / total * 100) if total > 0 else 0.0,
                }
            
            # Calculate average durations
            avg_durations = {}
            for key, total_duration in self.total_duration.items():
                count = self.request_count.get(key, 1)
                avg_durations[key] = total_duration / count if count > 0 else 0.0
            
            stats["average_durations"] = avg_durations
            
            return stats
    
    def reset(self):
        """Reset all metrics"""
        with self.lock:
            self.metrics.clear()
            self.request_count.clear()
            self.error_count.clear()
            self.total_tokens.clear()
            self.total_duration.clear()
            self.provider_availability.clear()
            self.logger.info("Metrics reset")


# Global metrics collector
_metrics_collector: Optional[MetricsCollector] = None


def get_metrics_collector() -> MetricsCollector:
    """Get or create metrics collector instance"""
    global _metrics_collector
    if _metrics_collector is None:
        _metrics_collector = MetricsCollector()
    return _metrics_collector


class MetricsContext:
    """Context manager for tracking request metrics"""
    
    def __init__(
        self,
        collector: MetricsCollector,
        provider: str,
        model: str,
    ):
        self.collector = collector
        self.provider = provider
        self.model = model
        self.start_time = time.time()
        self.success = False
        self.error_type = None
        self.tokens_used = None
        self.response_length = None
    
    def __enter__(self):
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        duration = time.time() - self.start_time
        self.success = exc_type is None
        
        if exc_type:
            self.error_type = exc_type.__name__
        
        self.collector.record_request(
            provider=self.provider,
            model=self.model,
            duration=duration,
            success=self.success,
            error_type=self.error_type,
            tokens_used=self.tokens_used,
            response_length=self.response_length,
        )
        
        return False  # Don't suppress exceptions
    
    def set_tokens(self, tokens: int):
        """Set tokens used"""
        self.tokens_used = tokens
    
    def set_response_length(self, length: int):
        """Set response length"""
        self.response_length = length

