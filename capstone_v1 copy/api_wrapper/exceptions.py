"""
Custom exception hierarchy for the Chatbot API Wrapper
"""


class ChatbotAPIError(Exception):
    """Base exception for all API wrapper errors"""
    
    def __init__(self, message: str, details: dict = None):
        super().__init__(message)
        self.message = message
        self.details = details or {}
    
    def __str__(self):
        if self.details:
            return f"{self.message} | Details: {self.details}"
        return self.message


class APIError(ChatbotAPIError):
    """Generic API request error"""
    pass


class RateLimitError(APIError):
    """Rate limit exceeded error"""
    
    def __init__(self, message: str = "Rate limit exceeded", retry_after: int = None, details: dict = None):
        super().__init__(message, details)
        self.retry_after = retry_after


class AuthenticationError(APIError):
    """Authentication/authorization error"""
    
    def __init__(self, message: str = "Authentication failed", details: dict = None):
        super().__init__(message, details)


class ModelNotFoundError(APIError):
    """Model not found or unavailable error"""
    
    def __init__(self, model: str, message: str = None, details: dict = None):
        if message is None:
            message = f"Model '{model}' not found or unavailable"
        super().__init__(message, details)
        self.model = model


class ConfigurationError(ChatbotAPIError):
    """Configuration error"""
    pass


class ValidationError(ChatbotAPIError):
    """Input validation error"""
    
    def __init__(self, message: str, field: str = None, details: dict = None):
        super().__init__(message, details)
        self.field = field


class NetworkError(APIError):
    """Network/connection error"""
    pass


class TimeoutError(APIError):
    """Request timeout error"""
    
    def __init__(self, message: str = "Request timeout", timeout: float = None, details: dict = None):
        super().__init__(message, details)
        self.timeout = timeout


class ProviderError(APIError):
    """Provider-specific error"""
    
    def __init__(self, provider: str, message: str, details: dict = None):
        super().__init__(message, details)
        self.provider = provider


class QuotaExceededError(RateLimitError):
    """API quota exceeded error"""
    
    def __init__(self, message: str = "API quota exceeded", details: dict = None):
        super().__init__(message, details=details)

