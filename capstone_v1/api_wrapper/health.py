"""
Health check utilities for monitoring system status
Includes dependency checks and HTTP endpoint support
"""

import time
import sys
import importlib
from typing import Dict, Any, Optional, List, Tuple
from datetime import datetime

from .logger import get_logger
from .metrics import get_metrics_collector

logger = get_logger("api_wrapper.health")


class HealthChecker:
    """Health check manager with dependency checks"""
    
    def __init__(self):
        self.logger = get_logger("api_wrapper.health")
        self.start_time = time.time()
        self.last_check: Optional[float] = None
        self.dependencies: Dict[str, bool] = {}
        self._check_dependencies()
    
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
    
    def _check_dependencies(self):
        """Check availability of required dependencies"""
        required_modules = [
            "requests",
            "openai",
            "transformers",
            "torch",
        ]
        
        optional_modules = [
            "pydantic",
            "tenacity",
            "cachetools",
            "structlog",
            "httpx",
        ]
        
        for module in required_modules:
            try:
                importlib.import_module(module)
                self.dependencies[module] = True
            except ImportError:
                self.dependencies[module] = False
                self.logger.warning(f"Required dependency {module} not available")
        
        for module in optional_modules:
            try:
                importlib.import_module(module)
                self.dependencies[module] = True
            except ImportError:
                self.dependencies[module] = False
    
    def check_dependencies(self) -> Dict[str, Any]:
        """
        Check dependency availability
        
        Returns:
            Dependency status dictionary
        """
        missing_required = [
            name for name, available in self.dependencies.items()
            if not available and name in ["requests", "openai", "transformers", "torch"]
        ]
        
        return {
            "dependencies": self.dependencies,
            "all_required_available": len(missing_required) == 0,
            "missing_required": missing_required,
            "timestamp": datetime.utcnow().isoformat(),
        }
    
    def get_http_response(self, endpoint: str = "health") -> Tuple[Dict[str, Any], int]:
        """
        Get HTTP response for health endpoints
        
        Args:
            endpoint: Endpoint type ('health', 'readiness', 'liveness')
        
        Returns:
            Tuple of (response_dict, status_code)
        """
        if endpoint == "health":
            health_data = self.check_health()
            status_code = 200 if health_data["status"] == "healthy" else (
                503 if health_data["status"] == "unhealthy" else 200
            )
            return health_data, status_code
        elif endpoint == "readiness":
            readiness_data = self.check_readiness()
            status_code = 200 if readiness_data["ready"] else 503
            return readiness_data, status_code
        elif endpoint == "liveness":
            liveness_data = self.check_liveness()
            status_code = 200 if liveness_data["alive"] else 503
            return liveness_data, status_code
        else:
            return {"error": "Unknown endpoint"}, 404


# Global health checker
_health_checker: Optional[HealthChecker] = None


def get_health_checker() -> HealthChecker:
    """Get or create health checker instance"""
    global _health_checker
    if _health_checker is None:
        _health_checker = HealthChecker()
    return _health_checker

