"""
OpenAI API Client for chatbot interactions
"""

import os
from typing import Dict, List, Optional, Union, Any, Iterator
import openai
from openai import OpenAI

from .config import (
    OPENAI_API_KEY,
    DEFAULT_TEMPERATURE,
    DEFAULT_MAX_TOKENS,
    DEFAULT_TOP_P,
)


class OpenAIClient:
    """
    Client for interacting with OpenAI's chat models
    """

    def __init__(self, api_key: Optional[str] = None, base_url: Optional[str] = None):
        """
        Initialize OpenAI client

        Args:
            api_key: OpenAI API key (if None, uses OPENAI_API_KEY env var)
            base_url: Custom base URL for API (optional, for compatible APIs)
        """
        self.api_key = api_key or OPENAI_API_KEY
        if not self.api_key:
            raise ValueError(
                "OpenAI API key is required. Set OPENAI_API_KEY environment variable or pass api_key parameter."
            )

        self.client = OpenAI(api_key=self.api_key, base_url=base_url)

    def chat(
        self,
        model: str,
        messages: Union[str, List[Dict[str, str]]],
        temperature: float = DEFAULT_TEMPERATURE,
        max_tokens: int = DEFAULT_MAX_TOKENS,
        top_p: float = DEFAULT_TOP_P,
        frequency_penalty: float = 0.0,
        presence_penalty: float = 0.0,
        **kwargs,
    ) -> Dict[str, Any]:
        """
        Generate a chat response using OpenAI model

        Args:
            model: OpenAI model identifier (e.g., 'gpt-4', 'gpt-3.5-turbo')
            messages: Either a string prompt or list of message dicts with 'role' and 'content'
            temperature: Sampling temperature (0.0 to 2.0)
            max_tokens: Maximum tokens to generate
            top_p: Nucleus sampling parameter
            frequency_penalty: Frequency penalty (-2.0 to 2.0)
            presence_penalty: Presence penalty (-2.0 to 2.0)
            **kwargs: Additional parameters for OpenAI API

        Returns:
            Dictionary with 'response' and metadata
        """
        # Format messages
        if isinstance(messages, str):
            formatted_messages = [{"role": "user", "content": messages}]
        else:
            formatted_messages = messages

        try:
            response = self.client.chat.completions.create(
                model=model,
                messages=formatted_messages,
                temperature=temperature,
                max_tokens=max_tokens,
                top_p=top_p,
                frequency_penalty=frequency_penalty,
                presence_penalty=presence_penalty,
                **kwargs,
            )

            return {
                "response": response.choices[0].message.content,
                "model": model,
                "provider": "openai",
                "usage": {
                    "prompt_tokens": response.usage.prompt_tokens,
                    "completion_tokens": response.usage.completion_tokens,
                    "total_tokens": response.usage.total_tokens,
                },
                "finish_reason": response.choices[0].finish_reason,
            }
        except Exception as e:
            raise Exception(f"OpenAI API request failed: {str(e)}")

    def stream_chat(
        self,
        model: str,
        messages: Union[str, List[Dict[str, str]]],
        temperature: float = DEFAULT_TEMPERATURE,
        max_tokens: int = DEFAULT_MAX_TOKENS,
        top_p: float = DEFAULT_TOP_P,
        **kwargs,
    ) -> Iterator[str]:
        """
        Stream chat responses (yields tokens as they're generated)

        Args:
            model: OpenAI model identifier
            messages: Either a string prompt or list of message dicts
            temperature: Sampling temperature
            max_tokens: Maximum tokens to generate
            top_p: Nucleus sampling parameter
            **kwargs: Additional parameters

        Yields:
            String chunks of the response
        """
        # Format messages
        if isinstance(messages, str):
            formatted_messages = [{"role": "user", "content": messages}]
        else:
            formatted_messages = messages

        try:
            stream = self.client.chat.completions.create(
                model=model,
                messages=formatted_messages,
                temperature=temperature,
                max_tokens=max_tokens,
                top_p=top_p,
                stream=True,
                **kwargs,
            )

            for chunk in stream:
                if chunk.choices[0].delta.content is not None:
                    yield chunk.choices[0].delta.content
        except Exception as e:
            raise Exception(f"OpenAI streaming request failed: {str(e)}")

    def list_available_models(self) -> List[str]:
        """List available OpenAI models"""
        from .config import OPENAI_CHATBOT_MODELS
        return list(OPENAI_CHATBOT_MODELS.keys())

    def get_model_info(self, model: str) -> Dict[str, Any]:
        """Get information about a specific model"""
        from .config import OPENAI_CHATBOT_MODELS
        return OPENAI_CHATBOT_MODELS.get(model, {})

