"""
Example demonstrating metrics collection and health checks
"""

from api_wrapper.metrics import get_metrics_collector, MetricsContext
from api_wrapper.health import get_health_checker
import time


def example_metrics_collection():
    """Demonstrate metrics collection"""
    print("=" * 60)
    print("Metrics Collection Example")
    print("=" * 60)
    
    collector = get_metrics_collector()
    
    # Simulate some API requests
    print("\n1. Simulating API requests...")
    for i in range(5):
        with MetricsContext(collector, "openai", "gpt-3.5-turbo") as ctx:
            time.sleep(0.1)  # Simulate request
            ctx.set_tokens(100 + i * 10)
            ctx.set_response_length(500 + i * 50)
            ctx.success = True
    
    # Record an error
    with MetricsContext(collector, "openai", "gpt-3.5-turbo") as ctx:
        time.sleep(0.05)
        ctx.success = False
        ctx.error_type = "RateLimitError"
    
    # Get statistics
    print("\n2. Current Statistics:")
    stats = collector.get_stats()
    print(f"   Total requests: {sum(stats['request_counts'].values())}")
    print(f"   Total errors: {sum(stats['error_counts'].values())}")
    print(f"   Provider availability:")
    for provider, avail in stats.get('provider_availability', {}).items():
        print(f"     {provider}: {avail['availability_percent']:.1f}%")
    
    # Export in different formats
    print("\n3. Prometheus Export (first 5 lines):")
    prometheus = collector.export_prometheus()
    for line in prometheus.split('\n')[:5]:
        if line.strip():
            print(f"   {line}")
    
    print("\n4. JSON Export:")
    json_output = collector.export_json()
    print(f"   {json_output[:200]}...")
    
    print("\n5. StatsD Export (first 3 lines):")
    statsd = collector.export_statsd()
    for line in statsd[:3]:
        print(f"   {line}")


def example_health_checks():
    """Demonstrate health checks"""
    print("\n" + "=" * 60)
    print("Health Checks Example")
    print("=" * 60)
    
    checker = get_health_checker()
    
    # Health check
    print("\n1. Health Check:")
    health = checker.check_health()
    print(f"   Status: {health['status']}")
    print(f"   Uptime: {health['uptime_seconds']:.1f} seconds")
    print(f"   Total requests: {health['metrics']['total_requests']}")
    print(f"   Error rate: {health['metrics']['error_rate_percent']:.1f}%")
    if health['issues']:
        print(f"   Issues: {', '.join(health['issues'])}")
    else:
        print("   Issues: None")
    
    # Readiness check
    print("\n2. Readiness Check:")
    readiness = checker.check_readiness()
    print(f"   Ready: {readiness['ready']}")
    print(f"   Timestamp: {readiness['timestamp']}")
    
    # Liveness check
    print("\n3. Liveness Check:")
    liveness = checker.check_liveness()
    print(f"   Alive: {liveness['alive']}")
    print(f"   Uptime: {liveness['uptime_seconds']:.1f} seconds")
    
    # Dependency check
    print("\n4. Dependency Check:")
    deps = checker.check_dependencies()
    print(f"   All required available: {deps['all_required_available']}")
    if deps['missing_required']:
        print(f"   Missing required: {', '.join(deps['missing_required'])}")
    print("   Dependencies:")
    for dep, available in deps['dependencies'].items():
        status = "✓" if available else "✗"
        print(f"     {status} {dep}")
    
    # HTTP response example
    print("\n5. HTTP Response Example:")
    status, code = checker.get_http_response('health')
    print(f"   Status code: {code}")
    print(f"   Response: {status['status']}")


def example_integration():
    """Example of integrating metrics and health in a web app"""
    print("\n" + "=" * 60)
    print("Integration Example (Flask-style)")
    print("=" * 60)
    
    print("""
# Flask/FastAPI integration example:

from flask import Flask, Response, jsonify
from api_wrapper.metrics import get_metrics_collector
from api_wrapper.health import get_health_checker

app = Flask(__name__)

@app.route('/metrics')
def metrics():
    collector = get_metrics_collector()
    return Response(
        collector.export_prometheus(),
        mimetype='text/plain'
    )

@app.route('/health')
def health():
    checker = get_health_checker()
    status, code = checker.get_http_response('health')
    return jsonify(status), code

@app.route('/health/readiness')
def readiness():
    checker = get_health_checker()
    status, code = checker.get_http_response('readiness')
    return jsonify(status), code

@app.route('/health/liveness')
def liveness():
    checker = get_health_checker()
    status, code = checker.get_http_response('liveness')
    return jsonify(status), code
    """)


if __name__ == "__main__":
    example_metrics_collection()
    example_health_checks()
    example_integration()
    
    print("\n" + "=" * 60)
    print("Examples completed!")
    print("=" * 60)

