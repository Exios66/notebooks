"""
Chatbot API Wrapper for HuggingFace and OpenAI
Provides a unified interface for interacting with various chatbot models
"""

from .chatbot_wrapper import ChatbotWrapper, Provider, Conversation
from .huggingface_client import HuggingFaceClient
from .openai_client import OpenAIClient

# Optional imports for additional functionality
try:
    from .starter_prompts import (  # noqa: F401
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
    from .dataset_loaders import (  # noqa: F401
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
    from .exceptions import (  # noqa: F401
        ChatbotAPIError,
        APIError,
        RateLimitError,
        AuthenticationError,
        ModelNotFoundError,
        ValidationError,
        NetworkError,
        TimeoutError,
    )
    from .logger import get_logger, setup_logger  # noqa: F401
    from .retry import exponential_backoff, RetryHandler  # noqa: F401
    from .rate_limiter import RateLimiter, get_rate_limiter  # noqa: F401
    from .cache import ResponseCache, get_cache  # noqa: F401
    from .metrics import MetricsCollector, get_metrics_collector  # noqa: F401
    from .health import HealthChecker, get_health_checker  # noqa: F401
    from .security import (  # noqa: F401
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
