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
from .logger import get_logger, RequestLogger
from .exceptions import (
    APIError,
    AuthenticationError,
    ModelNotFoundError,
    ProviderError,
    ValidationError,
)
# Production features - optional imports with graceful fallback
try:
    from .security import (
        validate_messages,
        validate_model_name,
        validate_temperature,
        validate_max_tokens,
    )
    from .retry import RetryHandler
    from .rate_limiter import get_rate_limiter
    from .cache import get_cache
    from .metrics import MetricsContext, get_metrics_collector
    from .settings import get_settings
    _PRODUCTION_FEATURES_AVAILABLE = True
except ImportError:
    _PRODUCTION_FEATURES_AVAILABLE = False
    # Define fallback functions
    def validate_messages(messages): return messages
    def validate_model_name(model): return model
    def validate_temperature(temp): return temp
    def validate_max_tokens(tokens): return tokens


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
        enable_retry: bool = True,
        enable_rate_limiting: bool = True,
        enable_caching: bool = True,
        enable_validation: bool = True,
        enable_metrics: bool = True,
    ):
        """
        Initialize the chatbot wrapper

        Args:
            huggingface_api_key: HuggingFace API key (optional)
            openai_api_key: OpenAI API key (optional)
            use_local_hf: Use local HuggingFace models instead of API
            hf_device: Device for local HuggingFace models ('cpu', 'cuda', 'auto')
            enable_retry: Enable automatic retry on failures (default: True)
            enable_rate_limiting: Enable rate limiting (default: True)
            enable_caching: Enable response caching (default: True)
            enable_validation: Enable input validation (default: True)
            enable_metrics: Enable metrics collection (default: True)
        """
        self.logger = get_logger("api_wrapper.chatbot_wrapper")
        self.hf_client: Optional[HuggingFaceClient] = None
        self.openai_client: Optional[OpenAIClient] = None
        
        # Initialize production features
        self.enable_retry = enable_retry and _PRODUCTION_FEATURES_AVAILABLE
        self.enable_rate_limiting = enable_rate_limiting and _PRODUCTION_FEATURES_AVAILABLE
        self.enable_caching = enable_caching and _PRODUCTION_FEATURES_AVAILABLE
        self.enable_validation = enable_validation and _PRODUCTION_FEATURES_AVAILABLE
        self.enable_metrics = enable_metrics and _PRODUCTION_FEATURES_AVAILABLE
        
        if _PRODUCTION_FEATURES_AVAILABLE:
            try:
                settings = get_settings()
                self.retry_handler = RetryHandler(
                    max_retries=settings.max_retries,
                    initial_delay=settings.initial_retry_delay,
                    max_delay=settings.max_retry_delay,
                    exponential_base=settings.retry_exponential_base,
                ) if self.enable_retry else None
                self.rate_limiter = get_rate_limiter() if self.enable_rate_limiting else None
                self.cache = get_cache() if self.enable_caching else None
                self.metrics_collector = get_metrics_collector() if self.enable_metrics else None
            except Exception as e:
                self.logger.warning(f"Failed to initialize some production features: {e}")
                self.retry_handler = None
                self.rate_limiter = None
                self.cache = None
                self.metrics_collector = None
        else:
            self.retry_handler = None
            self.rate_limiter = None
            self.cache = None
            self.metrics_collector = None
            self.logger.info("Production features not available. Install optional dependencies for full functionality.")

        # Initialize HuggingFace client if key is provided or local mode
        if huggingface_api_key or use_local_hf:
            try:
                self.hf_client = HuggingFaceClient(
                    api_key=huggingface_api_key, use_local=use_local_hf, device=hf_device
                )
                self.logger.info("HuggingFace client initialized successfully")
            except Exception as e:
                self.logger.warning(
                    f"Failed to initialize HuggingFace client: {e}",
                    exc_info=True
                )

        # Initialize OpenAI client if key is provided
        if openai_api_key:
            try:
                self.openai_client = OpenAIClient(api_key=openai_api_key)
                self.logger.info("OpenAI client initialized successfully")
            except Exception as e:
                self.logger.warning(
                    f"Failed to initialize OpenAI client: {e}",
                    exc_info=True
                )

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
        # Input validation
        if self.enable_validation:
            try:
                model = validate_model_name(model)
                messages = validate_messages(messages)
                temperature = validate_temperature(temperature)
                max_tokens = validate_max_tokens(max_tokens)
            except ValidationError as e:
                self.logger.error(f"Validation error: {e}")
                raise
        
        # Determine provider
        if provider == Provider.AUTO or provider == "auto":
            provider = self._detect_provider(model)
        else:
            provider = Provider(provider)
        
        provider_str = provider.value if isinstance(provider, Provider) else str(provider)
        
        # Check cache
        if self.enable_caching and self.cache:
            cache_key = {
                "provider": provider_str,
                "model": model,
                "messages": messages,
                "temperature": temperature,
                "max_tokens": max_tokens,
                **kwargs
            }
            cached_response = self.cache.get(
                provider=provider_str,
                model=model,
                messages=messages,
                temperature=temperature,
                max_tokens=max_tokens,
                **kwargs
            )
            if cached_response:
                self.logger.debug(f"Cache hit for {provider_str}:{model}")
                return cached_response
        
        # Rate limiting
        if self.enable_rate_limiting and self.rate_limiter:
            try:
                self.rate_limiter.acquire(
                    provider=provider_str,
                    model=model,
                    wait=True  # Wait for rate limit instead of failing
                )
            except Exception as e:
                self.logger.warning(f"Rate limiting error (continuing anyway): {e}")
        
        # Define the actual API call function
        def _make_api_call() -> Dict[str, Any]:
            if provider == Provider.HUGGINGFACE:
                if not self.hf_client:
                    raise AuthenticationError(
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
                    raise AuthenticationError(
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
                raise ProviderError(provider, f"Unknown provider: {provider}")
        
        # Execute with retry, metrics, and logging
        try:
            # Metrics context
            metrics_ctx = None
            if self.enable_metrics and self.metrics_collector:
                metrics_ctx = MetricsContext(
                    self.metrics_collector,
                    provider=provider_str,
                    model=model
                )
                metrics_ctx.__enter__()
            
            # Request logging
            with RequestLogger(
                self.logger, "chat", model, provider_str,
                temperature=temperature, max_tokens=max_tokens
            ):
                # Execute with retry if enabled
                if self.enable_retry and self.retry_handler:
                    response = self.retry_handler.execute(_make_api_call)
                else:
                    response = _make_api_call()
                
                # Update metrics
                if metrics_ctx:
                    if "usage" in response and isinstance(response["usage"], dict):
                        tokens = response["usage"].get("total_tokens")
                        if tokens:
                            metrics_ctx.set_tokens(tokens)
                    if "response" in response:
                        metrics_ctx.set_response_length(len(response["response"]))
            
            # Cache the response
            if self.enable_caching and self.cache:
                self.cache.set(
                    provider=provider_str,
                    model=model,
                    messages=messages,
                    response=response,
                    temperature=temperature,
                    max_tokens=max_tokens,
                    **kwargs
                )
            
            return response
            
        except Exception as e:
            # Update metrics on error
            if metrics_ctx:
                metrics_ctx.error_type = type(e).__name__
            raise
        finally:
            if metrics_ctx:
                metrics_ctx.__exit__(None, None, None)

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
        # Input validation
        if self.enable_validation:
            try:
                model = validate_model_name(model)
                messages = validate_messages(messages)
                temperature = validate_temperature(temperature)
                max_tokens = validate_max_tokens(max_tokens)
            except ValidationError as e:
                self.logger.error(f"Validation error: {e}")
                raise
        
        # Determine provider
        if provider == Provider.AUTO or provider == "auto":
            provider = self._detect_provider(model)
        else:
            provider = Provider(provider)
        
        # Rate limiting (for streaming, we still apply rate limiting)
        provider_str = provider.value if isinstance(provider, Provider) else str(provider)
        if self.enable_rate_limiting and self.rate_limiter:
            try:
                self.rate_limiter.acquire(
                    provider=provider_str,
                    model=model,
                    wait=True
                )
            except Exception as e:
                self.logger.warning(f"Rate limiting error (continuing anyway): {e}")

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
        Uses the comprehensive models registry if available

        Args:
            provider: Provider to list models for ('huggingface', 'openai', or None for all)

        Returns:
            Dictionary mapping provider names to lists of model identifiers
        """
        # Try to use models registry first
        try:
            from models.models_registry import list_models_by_provider as registry_list
            registry_models = {}
            
            if provider is None or provider == Provider.HUGGINGFACE or provider == "huggingface":
                hf_models = registry_list("huggingface")
                registry_models["huggingface"] = [m.model_id for m in hf_models]
            
            if provider is None or provider == Provider.OPENAI or provider == "openai":
                openai_models = registry_list("openai")
                registry_models["openai"] = [m.model_id for m in openai_models]
            
            if registry_models:
                return registry_models
        except ImportError:
            # Models registry not available, fall back to basic config
            pass
        
        # Fallback to basic config
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
        Uses the comprehensive models registry if available, falls back to basic config

        Args:
            model: Model identifier

        Returns:
            Dictionary with model information
        """
        # Try to use models registry first (comprehensive information)
        try:
            from models.models_registry import get_model_info as registry_get_info
            model_info = registry_get_info(model)
            if model_info:
                # Convert ModelInfo dataclass to dict for compatibility
                result = {
                    "model_id": model_info.model_id,
                    "name": model_info.name,
                    "provider": model_info.provider,
                    "type": model_info.type.value,
                    "description": model_info.description,
                    "access_method": model_info.access_method.value,
                }
                if model_info.api_endpoint:
                    result["api_endpoint"] = {
                        "url": model_info.api_endpoint.url,
                        "method": model_info.api_endpoint.method,
                        "auth_required": model_info.api_endpoint.auth_required,
                        "rate_limit": model_info.api_endpoint.rate_limit,
                    }
                if model_info.specs:
                    result["specs"] = {
                        "parameters": model_info.specs.parameters,
                        "context_window": model_info.specs.context_window,
                        "architecture": model_info.specs.architecture,
                    }
                result["license"] = model_info.license.value if model_info.license else None
                result["free_tier_available"] = model_info.free_tier_available
                result["recommended_use_cases"] = model_info.recommended_use_cases
                result["limitations"] = model_info.limitations
                result["documentation_url"] = model_info.documentation_url
                return result
        except ImportError:
            # Models registry not available, fall back to basic config
            pass
        
        # Fallback to basic config
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

