"""
Unit tests for ChatbotWrapper
"""

import pytest
from unittest.mock import Mock, patch, MagicMock

from api_wrapper import ChatbotWrapper, Provider
from api_wrapper.exceptions import (
    AuthenticationError,
    ModelNotFoundError,
    ProviderError,
    APIError,
)


class TestChatbotWrapper:
    """Test cases for ChatbotWrapper"""
    
    def test_initialization(self):
        """Test wrapper initialization"""
        wrapper = ChatbotWrapper(
            openai_api_key="test-key",
            huggingface_api_key="test-hf-key",
        )
        assert wrapper is not None
        assert wrapper.openai_client is not None
        assert wrapper.hf_client is not None
    
    def test_initialization_no_keys(self):
        """Test initialization without API keys"""
        wrapper = ChatbotWrapper()
        assert wrapper.openai_client is None
        assert wrapper.hf_client is None
    
    def test_detect_provider_openai(self):
        """Test provider detection for OpenAI models"""
        wrapper = ChatbotWrapper()
        provider = wrapper._detect_provider("gpt-3.5-turbo")
        assert provider == Provider.OPENAI
    
    def test_detect_provider_huggingface(self):
        """Test provider detection for HuggingFace models"""
        wrapper = ChatbotWrapper()
        provider = wrapper._detect_provider("mistralai/Mistral-7B-Instruct-v0.2")
        assert provider == Provider.HUGGINGFACE
    
    def test_detect_provider_auto(self):
        """Test auto provider detection"""
        wrapper = ChatbotWrapper()
        # Test OpenAI
        provider = wrapper._detect_provider("gpt-4")
        assert provider == Provider.OPENAI
        
        # Test HuggingFace
        provider = wrapper._detect_provider("meta-llama/Llama-2-7b-chat-hf")
        assert provider == Provider.HUGGINGFACE
    
    @patch('api_wrapper.chatbot_wrapper.OpenAIClient')
    def test_chat_openai_success(self, mock_openai_class):
        """Test successful OpenAI chat"""
        mock_client = MagicMock()
        mock_client.chat.return_value = {
            "response": "Hello!",
            "model": "gpt-3.5-turbo",
            "provider": "openai",
        }
        mock_openai_class.return_value = mock_client
        
        wrapper = ChatbotWrapper(openai_api_key="test-key")
        response = wrapper.chat(
            model="gpt-3.5-turbo",
            messages="Hello",
            provider="openai",
        )
        
        assert response["response"] == "Hello!"
        mock_client.chat.assert_called_once()
    
    @patch('api_wrapper.chatbot_wrapper.HuggingFaceClient')
    def test_chat_huggingface_success(self, mock_hf_class):
        """Test successful HuggingFace chat"""
        mock_client = MagicMock()
        mock_client.chat.return_value = {
            "response": "Hello!",
            "model": "mistralai/Mistral-7B-Instruct-v0.2",
            "provider": "huggingface",
        }
        mock_hf_class.return_value = mock_client
        
        wrapper = ChatbotWrapper(huggingface_api_key="test-key")
        response = wrapper.chat(
            model="mistralai/Mistral-7B-Instruct-v0.2",
            messages="Hello",
            provider="huggingface",
        )
        
        assert response["response"] == "Hello!"
        mock_client.chat.assert_called_once()
    
    def test_chat_no_client(self):
        """Test chat without initialized client"""
        wrapper = ChatbotWrapper()
        
        with pytest.raises(AuthenticationError):
            wrapper.chat(
                model="gpt-3.5-turbo",
                messages="Hello",
            )
    
    def test_conversation_creation(self):
        """Test conversation context creation"""
        wrapper = ChatbotWrapper(openai_api_key="test-key")
        conv = wrapper.conversation(
            model="gpt-3.5-turbo",
            system_prompt="You are a helpful assistant.",
        )
        
        assert conv is not None
        assert conv.model == "gpt-3.5-turbo"
        assert len(conv.messages) == 1
        assert conv.messages[0]["role"] == "system"
    
    def test_list_models(self):
        """Test listing available models"""
        wrapper = ChatbotWrapper()
        models = wrapper.list_models()
        
        assert "openai" in models
        assert "huggingface" in models
        assert len(models["openai"]) > 0
        assert len(models["huggingface"]) > 0
    
    def test_get_model_info(self):
        """Test getting model information"""
        wrapper = ChatbotWrapper()
        info = wrapper.get_model_info("gpt-3.5-turbo")
        
        assert "description" in info
        assert info["provider"] == "openai"

