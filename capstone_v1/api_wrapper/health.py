"""
Health check utilities for monitoring system status
"""

import time
from typing import Dict, Any, Optional
from datetime import datetime

from .logger import get_logger
from .metrics import get_metrics_collector

logger = get_logger("api_wrapper.health")


class HealthChecker:
    """Health check manager"""
    
    def __init__(self):
        self.logger = get_logger("api_wrapper.health")
        self.start_time = time.time()
        self.last_check: Optional[float] = None
    
    def check_health(self) -> Dict[str, Any]:
        """
        Perform health check
        
        Returns:
            Health status dictionary
        """
        self.last_check = time.time()
        uptime = self.last_check - self.start_time
        
        # Get metrics
        metrics = get_metrics_collector()
        stats = metrics.get_stats()
        
        # Determine overall health
        health_status = "healthy"
        issues = []
        
        # Check provider availability
        for provider, availability in stats.get("provider_availability", {}).items():
            avail_pct = availability.get("availability_percent", 0.0)
            if avail_pct < 95.0 and availability.get("total_requests", 0) > 10:
                health_status = "degraded"
                issues.append(f"{provider} availability is {avail_pct:.1f}%")
        
        # Check error rates
        total_requests = sum(stats.get("request_counts", {}).values())
        total_errors = sum(stats.get("error_counts", {}).values())
        if total_requests > 0:
            error_rate = (total_errors / total_requests) * 100
            if error_rate > 10.0:
                health_status = "unhealthy"
                issues.append(f"Error rate is {error_rate:.1f}%")
        
        return {
            "status": health_status,
            "uptime_seconds": uptime,
            "timestamp": datetime.utcnow().isoformat(),
            "metrics": {
                "total_requests": total_requests,
                "total_errors": total_errors,
                "error_rate_percent": (total_errors / total_requests * 100) if total_requests > 0 else 0.0,
            },
            "provider_availability": stats.get("provider_availability", {}),
            "issues": issues,
        }
    
    def check_readiness(self) -> Dict[str, Any]:
        """
        Check if system is ready to serve requests
        
        Returns:
            Readiness status
        """
        return {
            "ready": True,
            "timestamp": datetime.utcnow().isoformat(),
        }
    
    def check_liveness(self) -> Dict[str, Any]:
        """
        Check if system is alive
        
        Returns:
            Liveness status
        """
        return {
            "alive": True,
            "uptime_seconds": time.time() - self.start_time,
            "timestamp": datetime.utcnow().isoformat(),
        }


# Global health checker
_health_checker: Optional[HealthChecker] = None


def get_health_checker() -> HealthChecker:
    """Get or create health checker instance"""
    global _health_checker
    if _health_checker is None:
        _health_checker = HealthChecker()
    return _health_checker

