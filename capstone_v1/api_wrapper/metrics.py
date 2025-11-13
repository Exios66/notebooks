"""
Metrics collection for monitoring API usage and performance
Supports Prometheus and StatsD export formats
"""

import time
from typing import Dict, Any, Optional, List
from collections import defaultdict
from dataclasses import dataclass
import threading
import json

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

    def export_prometheus(self) -> str:
        """
        Export metrics in Prometheus format

        Returns:
            Prometheus-formatted metrics string
        """
        with self.lock:
            stats = self.get_stats()
            lines = []

            # Request counts
            for key, count in stats.get("request_counts", {}).items():
                provider, model = key.split(":", 1) if ":" in key else (key, "unknown")
                lines.append(
                    f'api_wrapper_requests_total{{provider="{provider}",model="{model}"}} {count}'
                )

            # Error counts
            for key, count in stats.get("error_counts", {}).items():
                if ":" in key:
                    parts = key.split(":")
                    if len(parts) == 2:
                        provider, model = parts
                        error_type = "unknown"
                    else:
                        provider, model, error_type = parts
                    lines.append(
                        f'api_wrapper_errors_total{{provider="{provider}",model="{model}",error_type="{error_type}"}} {count}'
                    )

            # Token usage
            for key, tokens in stats.get("total_tokens", {}).items():
                provider, model = key.split(":", 1) if ":" in key else (key, "unknown")
                lines.append(
                    f'api_wrapper_tokens_total{{provider="{provider}",model="{model}"}} {tokens}'
                )

            # Average durations
            for key, duration in stats.get("average_durations", {}).items():
                provider, model = key.split(":", 1) if ":" in key else (key, "unknown")
                lines.append(
                    f'api_wrapper_request_duration_seconds{{provider="{provider}",model="{model}"}} {duration:.4f}'
                )

            # Provider availability
            for provider, availability in stats.get("provider_availability", {}).items():
                avail_pct = availability.get("availability_percent", 0.0)
                lines.append(
                    f'api_wrapper_provider_availability{{provider="{provider}"}} {avail_pct:.2f}'
                )

            return "\n".join(lines) + "\n"

    def export_json(self) -> str:
        """
        Export metrics as JSON

        Returns:
            JSON-formatted metrics string
        """
        with self.lock:
            stats = self.get_stats()
            return json.dumps(stats, indent=2)

    def export_statsd(self) -> List[str]:
        """
        Export metrics in StatsD format

        Returns:
            List of StatsD metric strings
        """
        with self.lock:
            stats = self.get_stats()
            lines = []
            timestamp = int(time.time())

            # Request counts
            for key, count in stats.get("request_counts", {}).items():
                provider, model = key.split(":", 1) if ":" in key else (key, "unknown")
                lines.append(
                    f'api_wrapper.requests.{provider}.{model}:{count}|c|#{timestamp}'
                )

            # Error counts
            for key, count in stats.get("error_counts", {}).items():
                if ":" in key:
                    parts = key.split(":")
                    if len(parts) == 2:
                        provider, model = parts
                        error_type = "unknown"
                    else:
                        provider, model, error_type = parts
                    lines.append(
                        f'api_wrapper.errors.{provider}.{model}.{error_type}:{count}|c|#{timestamp}'
                    )

            # Average durations
            for key, duration in stats.get("average_durations", {}).items():
                provider, model = key.split(":", 1) if ":" in key else (key, "unknown")
                lines.append(
                    f'api_wrapper.duration.{provider}.{model}:{duration:.4f}|ms|#{timestamp}'
                )

            return lines


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
