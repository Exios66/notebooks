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

