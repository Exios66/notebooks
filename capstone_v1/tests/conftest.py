"""
Pytest configuration and fixtures
"""

import pytest
from unittest.mock import Mock, MagicMock
from typing import Dict, Any

from api_wrapper import ChatbotWrapper
from api_wrapper.exceptions import APIError, RateLimitError


@pytest.fixture
def mock_openai_response():
    """Mock OpenAI API response"""
    return {
        "response": "This is a test response",
        "model": "gpt-3.5-turbo",
        "provider": "openai",
        "usage": {
            "prompt_tokens": 10,
            "completion_tokens": 8,
            "total_tokens": 18,
        },
        "finish_reason": "stop",
    }


@pytest.fixture
def mock_huggingface_response():
    """Mock HuggingFace API response"""
    return {
        "response": "This is a test response",
        "model": "mistralai/Mistral-7B-Instruct-v0.2",
        "provider": "huggingface",
        "method": "api",
    }


@pytest.fixture
def chatbot_wrapper():
    """Create a ChatbotWrapper instance for testing"""
    return ChatbotWrapper(
        openai_api_key="test-openai-key",
        huggingface_api_key="test-hf-key",
    )


@pytest.fixture
def mock_openai_client(monkeypatch):
    """Mock OpenAI client"""
    mock_client = MagicMock()
    monkeypatch.setattr("api_wrapper.openai_client.OpenAIClient", lambda *args, **kwargs: mock_client)
    return mock_client


@pytest.fixture
def mock_huggingface_client(monkeypatch):
    """Mock HuggingFace client"""
    mock_client = MagicMock()
    monkeypatch.setattr("api_wrapper.huggingface_client.HuggingFaceClient", lambda *args, **kwargs: mock_client)
    return mock_client

