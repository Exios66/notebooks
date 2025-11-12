"""
Chatbot API Wrapper for HuggingFace and OpenAI
Provides a unified interface for interacting with various chatbot models
"""

from .chatbot_wrapper import ChatbotWrapper, Provider, Conversation
from .huggingface_client import HuggingFaceClient
from .openai_client import OpenAIClient

# Optional imports for additional functionality
try:
    from .starter_prompts import (
        get_prompt,
        list_available_prompts,
        ALL_PROMPTS,
        GENERAL_ASSISTANT,
        CODING_ASSISTANT,
        DATA_SCIENCE_ASSISTANT,
    )
    _PROMPTS_AVAILABLE = True
except ImportError:
    _PROMPTS_AVAILABLE = False

try:
    from .dataset_loaders import (
        DatasetLoader,
        get_available_datasets,
        HUGGINGFACE_CHAT_DATASETS,
        SEABORN_DATASETS,
        SKLEARN_DATASETS,
        OPENML_DATASETS,
    )
    _DATASETS_AVAILABLE = True
except ImportError:
    _DATASETS_AVAILABLE = False

# Production features
try:
    from .exceptions import (
        ChatbotAPIError,
        APIError,
        RateLimitError,
        AuthenticationError,
        ModelNotFoundError,
        ValidationError,
        NetworkError,
        TimeoutError,
    )
    from .logger import get_logger, setup_logger
    from .retry import exponential_backoff, RetryHandler
    from .rate_limiter import RateLimiter, get_rate_limiter
    from .cache import ResponseCache, get_cache
    from .metrics import MetricsCollector, get_metrics_collector
    from .health import HealthChecker, get_health_checker
    from .security import (
        validate_message,
        validate_messages,
        validate_model_name,
        validate_temperature,
        validate_max_tokens,
    )
    _PRODUCTION_AVAILABLE = True
except ImportError:
    _PRODUCTION_AVAILABLE = False

__version__ = "1.0.0"
__all__ = [
    "ChatbotWrapper",
    "HuggingFaceClient",
    "OpenAIClient",
    "Provider",
    "Conversation",
]

# Add optional exports if available
if _PROMPTS_AVAILABLE:
    __all__.extend([
        "get_prompt",
        "list_available_prompts",
        "ALL_PROMPTS",
        "GENERAL_ASSISTANT",
        "CODING_ASSISTANT",
        "DATA_SCIENCE_ASSISTANT",
    ])

if _DATASETS_AVAILABLE:
    __all__.extend([
        "DatasetLoader",
        "get_available_datasets",
        "HUGGINGFACE_CHAT_DATASETS",
        "SEABORN_DATASETS",
        "SKLEARN_DATASETS",
        "OPENML_DATASETS",
    ])

if _PRODUCTION_AVAILABLE:
    __all__.extend([
        "ChatbotAPIError",
        "APIError",
        "RateLimitError",
        "AuthenticationError",
        "ModelNotFoundError",
        "ValidationError",
        "NetworkError",
        "TimeoutError",
        "get_logger",
        "setup_logger",
        "exponential_backoff",
        "RetryHandler",
        "RateLimiter",
        "get_rate_limiter",
        "ResponseCache",
        "get_cache",
        "MetricsCollector",
        "get_metrics_collector",
        "HealthChecker",
        "get_health_checker",
        "validate_message",
        "validate_messages",
        "validate_model_name",
        "validate_temperature",
        "validate_max_tokens",
    ])

