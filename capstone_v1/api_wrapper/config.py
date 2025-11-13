"""
Configuration module for API credentials and model settings

For comprehensive model information including full endpoints, specifications,
licensing, and use cases, see the models registry:
- models/models_registry.py (Python module)
- models/models_registry.json (JSON export)
- models/README.md (Documentation)
"""

import os
from typing import Dict, Optional

# HuggingFace Configuration
HUGGINGFACE_API_KEY: Optional[str] = os.getenv("HUGGINGFACE_API_KEY")
HUGGINGFACE_API_URL: str = "https://api-inference.huggingface.co/models"

# OpenAI Configuration
OPENAI_API_KEY: Optional[str] = os.getenv("OPENAI_API_KEY")
OPENAI_API_BASE: str = "https://api.openai.com/v1"

# Specialized Chatbot Models
HUGGINGFACE_CHATBOT_MODELS: Dict[str, Dict] = {
    "meta-llama/Llama-2-7b-chat-hf": {
        "name": "Llama 2 7B Chat",
        "provider": "huggingface",
        "type": "inference",
        "description": "Meta's Llama 2 7B chat model",
    },
    "meta-llama/Llama-2-13b-chat-hf": {
        "name": "Llama 2 13B Chat",
        "provider": "huggingface",
        "type": "inference",
        "description": "Meta's Llama 2 13B chat model",
    },
    "mistralai/Mistral-7B-Instruct-v0.2": {
        "name": "Mistral 7B Instruct",
        "provider": "huggingface",
        "type": "inference",
        "description": "Mistral AI's 7B instruction-tuned model",
    },
    "microsoft/DialoGPT-large": {
        "name": "DialoGPT Large",
        "provider": "huggingface",
        "type": "inference",
        "description": "Microsoft's conversational AI model",
    },
    "google/flan-t5-xxl": {
        "name": "FLAN-T5 XXL",
        "provider": "huggingface",
        "type": "inference",
        "description": "Google's instruction-tuned T5 model",
    },
    "HuggingFaceH4/zephyr-7b-beta": {
        "name": "Zephyr 7B Beta",
        "provider": "huggingface",
        "type": "inference",
        "description": "HuggingFace's Zephyr instruction-tuned model",
    },
    "meta-llama/Meta-Llama-3-8B-Instruct": {
        "name": "Llama 3 8B Instruct",
        "provider": "huggingface",
        "type": "inference",
        "description": "Meta's Llama 3 8B instruction model",
    },
}

OPENAI_CHATBOT_MODELS: Dict[str, Dict] = {
    "gpt-4": {
        "name": "GPT-4",
        "provider": "openai",
        "description": "OpenAI's most capable model",
    },
    "gpt-4-turbo": {
        "name": "GPT-4 Turbo",
        "provider": "openai",
        "description": "Faster and more capable GPT-4 variant",
    },
    "gpt-4-turbo-preview": {
        "name": "GPT-4 Turbo Preview",
        "provider": "openai",
        "description": "Preview version of GPT-4 Turbo",
    },
    "gpt-3.5-turbo": {
        "name": "GPT-3.5 Turbo",
        "provider": "openai",
        "description": "Fast and efficient GPT-3.5 model",
    },
    "gpt-3.5-turbo-16k": {
        "name": "GPT-3.5 Turbo 16K",
        "provider": "openai",
        "description": "GPT-3.5 with extended context window",
    },
}

# Default model parameters
DEFAULT_TEMPERATURE: float = 0.7
DEFAULT_MAX_TOKENS: int = 512
DEFAULT_TOP_P: float = 0.9
DEFAULT_TOP_K: int = 50


def get_model_registry():
    """
    Get the comprehensive models registry with full information and endpoints.
    
    Returns:
        Dict containing all model information from the models registry
        
    Example:
        >>> from api_wrapper.config import get_model_registry
        >>> registry = get_model_registry()
        >>> model_info = registry.get_model_info("gpt-3.5-turbo")
    """
    try:
        from models.models_registry import (
            get_model_info,
            list_models_by_provider,
            list_models_by_type,
            search_models,
            get_free_models,
            get_local_models,
            ALL_MODELS,
        )
        return {
            "get_model_info": get_model_info,
            "list_models_by_provider": list_models_by_provider,
            "list_models_by_type": list_models_by_type,
            "search_models": search_models,
            "get_free_models": get_free_models,
            "get_local_models": get_local_models,
            "ALL_MODELS": ALL_MODELS,
        }
    except ImportError:
        # Fallback if models registry is not available
        return None
