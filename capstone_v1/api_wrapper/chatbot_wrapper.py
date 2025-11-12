"""
Unified Chatbot Wrapper for HuggingFace and OpenAI
Provides a single interface for interacting with multiple chatbot providers
"""

from typing import Dict, List, Optional, Union, Any, Iterator
from enum import Enum

from .huggingface_client import HuggingFaceClient
from .openai_client import OpenAIClient
from .config import (
    HUGGINGFACE_CHATBOT_MODELS,
    OPENAI_CHATBOT_MODELS,
    DEFAULT_TEMPERATURE,
    DEFAULT_MAX_TOKENS,
)


class Provider(str, Enum):
    """Supported chatbot providers"""
    HUGGINGFACE = "huggingface"
    OPENAI = "openai"
    AUTO = "auto"  # Automatically select based on model name


class ChatbotWrapper:
    """
    Unified wrapper for chatbot interactions across multiple providers
    """

    def __init__(
        self,
        huggingface_api_key: Optional[str] = None,
        openai_api_key: Optional[str] = None,
        use_local_hf: bool = False,
        hf_device: str = "auto",
    ):
        """
        Initialize the chatbot wrapper

        Args:
            huggingface_api_key: HuggingFace API key (optional)
            openai_api_key: OpenAI API key (optional)
            use_local_hf: Use local HuggingFace models instead of API
            hf_device: Device for local HuggingFace models ('cpu', 'cuda', 'auto')
        """
        self.hf_client: Optional[HuggingFaceClient] = None
        self.openai_client: Optional[OpenAIClient] = None

        # Initialize HuggingFace client if key is provided or local mode
        if huggingface_api_key or use_local_hf:
            try:
                self.hf_client = HuggingFaceClient(
                    api_key=huggingface_api_key, use_local=use_local_hf, device=hf_device
                )
            except Exception as e:
                print(f"Warning: Failed to initialize HuggingFace client: {e}")

        # Initialize OpenAI client if key is provided
        if openai_api_key:
            try:
                self.openai_client = OpenAIClient(api_key=openai_api_key)
            except Exception as e:
                print(f"Warning: Failed to initialize OpenAI client: {e}")

    def _detect_provider(self, model: str) -> Provider:
        """
        Detect which provider a model belongs to

        Args:
            model: Model identifier

        Returns:
            Provider enum
        """
        if model in HUGGINGFACE_CHATBOT_MODELS:
            return Provider.HUGGINGFACE
        elif model in OPENAI_CHATBOT_MODELS:
            return Provider.OPENAI
        else:
            # Try to infer from model name
            if "gpt" in model.lower() or "openai" in model.lower():
                return Provider.OPENAI
            else:
                return Provider.HUGGINGFACE

    def chat(
        self,
        model: str,
        messages: Union[str, List[Dict[str, str]]],
        provider: Union[Provider, str] = Provider.AUTO,
        temperature: float = DEFAULT_TEMPERATURE,
        max_tokens: int = DEFAULT_MAX_TOKENS,
        **kwargs,
    ) -> Dict[str, Any]:
        """
        Generate a chat response using the specified model

        Args:
            model: Model identifier
            messages: Either a string prompt or list of message dicts with 'role' and 'content'
            provider: Provider to use ('huggingface', 'openai', or 'auto')
            temperature: Sampling temperature
            max_tokens: Maximum tokens to generate
            **kwargs: Additional provider-specific parameters

        Returns:
            Dictionary with 'response' and metadata

        Example:
            >>> wrapper = ChatbotWrapper()
            >>> response = wrapper.chat(
            ...     model="gpt-3.5-turbo",
            ...     messages="Hello, how are you?",
            ...     temperature=0.7
            ... )
            >>> print(response['response'])
        """
        # Determine provider
        if provider == Provider.AUTO or provider == "auto":
            provider = self._detect_provider(model)
        else:
            provider = Provider(provider)

        # Route to appropriate client
        if provider == Provider.HUGGINGFACE:
            if not self.hf_client:
                raise ValueError(
                    "HuggingFace client not initialized. Provide huggingface_api_key or set use_local_hf=True."
                )
            return self.hf_client.chat(
                model_id=model,
                messages=messages,
                temperature=temperature,
                max_tokens=max_tokens,
                **kwargs,
            )
        elif provider == Provider.OPENAI:
            if not self.openai_client:
                raise ValueError(
                    "OpenAI client not initialized. Provide openai_api_key."
                )
            return self.openai_client.chat(
                model=model,
                messages=messages,
                temperature=temperature,
                max_tokens=max_tokens,
                **kwargs,
            )
        else:
            raise ValueError(f"Unknown provider: {provider}")

    def stream_chat(
        self,
        model: str,
        messages: Union[str, List[Dict[str, str]]],
        provider: Union[Provider, str] = Provider.AUTO,
        temperature: float = DEFAULT_TEMPERATURE,
        max_tokens: int = DEFAULT_MAX_TOKENS,
        **kwargs,
    ) -> Iterator[str]:
        """
        Stream chat responses (yields tokens as they're generated)

        Args:
            model: Model identifier
            messages: Either a string prompt or list of message dicts
            provider: Provider to use ('huggingface', 'openai', or 'auto')
            temperature: Sampling temperature
            max_tokens: Maximum tokens to generate
            **kwargs: Additional provider-specific parameters

        Yields:
            String chunks of the response

        Example:
            >>> wrapper = ChatbotWrapper()
            >>> for chunk in wrapper.stream_chat(
            ...     model="gpt-3.5-turbo",
            ...     messages="Tell me a story"
            ... ):
            ...     print(chunk, end='', flush=True)
        """
        # Determine provider
        if provider == Provider.AUTO or provider == "auto":
            provider = self._detect_provider(model)
        else:
            provider = Provider(provider)

        # Route to appropriate client
        if provider == Provider.HUGGINGFACE:
            if not self.hf_client:
                raise ValueError(
                    "HuggingFace client not initialized. Provide huggingface_api_key or set use_local_hf=True."
                )
            yield from self.hf_client.stream_chat(
                model_id=model,
                messages=messages,
                temperature=temperature,
                max_tokens=max_tokens,
                **kwargs,
            )
        elif provider == Provider.OPENAI:
            if not self.openai_client:
                raise ValueError(
                    "OpenAI client not initialized. Provide openai_api_key."
                )
            yield from self.openai_client.stream_chat(
                model=model,
                messages=messages,
                temperature=temperature,
                max_tokens=max_tokens,
                **kwargs,
            )
        else:
            raise ValueError(f"Unknown provider: {provider}")

    def list_models(self, provider: Optional[Union[Provider, str]] = None) -> Dict[str, List[str]]:
        """
        List available models for the specified provider(s)

        Args:
            provider: Provider to list models for ('huggingface', 'openai', or None for all)

        Returns:
            Dictionary mapping provider names to lists of model identifiers
        """
        models = {}

        if provider is None or provider == Provider.HUGGINGFACE or provider == "huggingface":
            if self.hf_client:
                models["huggingface"] = self.hf_client.list_available_models()
            else:
                models["huggingface"] = list(HUGGINGFACE_CHATBOT_MODELS.keys())

        if provider is None or provider == Provider.OPENAI or provider == "openai":
            if self.openai_client:
                models["openai"] = self.openai_client.list_available_models()
            else:
                models["openai"] = list(OPENAI_CHATBOT_MODELS.keys())

        return models

    def get_model_info(self, model: str) -> Dict[str, Any]:
        """
        Get information about a specific model

        Args:
            model: Model identifier

        Returns:
            Dictionary with model information
        """
        if model in HUGGINGFACE_CHATBOT_MODELS:
            return HUGGINGFACE_CHATBOT_MODELS[model]
        elif model in OPENAI_CHATBOT_MODELS:
            return OPENAI_CHATBOT_MODELS[model]
        else:
            return {"error": "Model not found in configuration"}

    def conversation(
        self,
        model: str,
        system_prompt: Optional[str] = None,
        provider: Union[Provider, str] = Provider.AUTO,
        temperature: float = DEFAULT_TEMPERATURE,
        max_tokens: int = DEFAULT_MAX_TOKENS,
        **kwargs,
    ) -> "Conversation":
        """
        Create a conversation context for multi-turn interactions

        Args:
            model: Model identifier
            system_prompt: Optional system prompt to set context
            provider: Provider to use
            temperature: Sampling temperature
            max_tokens: Maximum tokens per response
            **kwargs: Additional parameters

        Returns:
            Conversation object for managing multi-turn chats

        Example:
            >>> wrapper = ChatbotWrapper()
            >>> conv = wrapper.conversation(
            ...     model="gpt-3.5-turbo",
            ...     system_prompt="You are a helpful assistant."
            ... )
            >>> conv.send("Hello!")
            >>> conv.send("What's the weather?")
        """
        return Conversation(
            wrapper=self,
            model=model,
            system_prompt=system_prompt,
            provider=provider,
            temperature=temperature,
            max_tokens=max_tokens,
            **kwargs,
        )


class Conversation:
    """
    Conversation context for multi-turn chatbot interactions
    """

    def __init__(
        self,
        wrapper: ChatbotWrapper,
        model: str,
        system_prompt: Optional[str] = None,
        provider: Union[Provider, str] = Provider.AUTO,
        temperature: float = DEFAULT_TEMPERATURE,
        max_tokens: int = DEFAULT_MAX_TOKENS,
        **kwargs,
    ):
        """
        Initialize a conversation

        Args:
            wrapper: ChatbotWrapper instance
            model: Model identifier
            system_prompt: Optional system prompt
            provider: Provider to use
            temperature: Sampling temperature
            max_tokens: Maximum tokens per response
            **kwargs: Additional parameters
        """
        self.wrapper = wrapper
        self.model = model
        self.provider = provider
        self.temperature = temperature
        self.max_tokens = max_tokens
        self.kwargs = kwargs
        self.messages: List[Dict[str, str]] = []

        if system_prompt:
            self.messages.append({"role": "system", "content": system_prompt})

    def send(self, message: str) -> str:
        """
        Send a message and get a response

        Args:
            message: User message

        Returns:
            Assistant response
        """
        self.messages.append({"role": "user", "content": message})

        response = self.wrapper.chat(
            model=self.model,
            messages=self.messages,
            provider=self.provider,
            temperature=self.temperature,
            max_tokens=self.max_tokens,
            **self.kwargs,
        )

        assistant_message = response["response"]
        self.messages.append({"role": "assistant", "content": assistant_message})

        return assistant_message

    def stream_send(self, message: str) -> Iterator[str]:
        """
        Send a message and stream the response

        Args:
            message: User message

        Yields:
            Response chunks
        """
        self.messages.append({"role": "user", "content": message})

        full_response = ""
        for chunk in self.wrapper.stream_chat(
            model=self.model,
            messages=self.messages,
            provider=self.provider,
            temperature=self.temperature,
            max_tokens=self.max_tokens,
            **self.kwargs,
        ):
            full_response += chunk
            yield chunk

        self.messages.append({"role": "assistant", "content": full_response})

    def reset(self):
        """Reset the conversation history"""
        system_msg = None
        if self.messages and self.messages[0].get("role") == "system":
            system_msg = self.messages[0]["content"]
        self.messages = []
        if system_msg:
            self.messages.append({"role": "system", "content": system_msg})

    def get_history(self) -> List[Dict[str, str]]:
        """Get the conversation history"""
        return self.messages.copy()

