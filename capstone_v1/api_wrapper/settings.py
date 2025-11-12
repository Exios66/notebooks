"""
Pydantic-based configuration management with validation
"""

import os
from typing import Optional
from enum import Enum

try:
    from pydantic import BaseSettings, Field, validator
    PYDANTIC_AVAILABLE = True
except ImportError:
    PYDANTIC_AVAILABLE = False
    BaseSettings = object
    Field = None
    validator = None

from .logger import get_logger

logger = get_logger("api_wrapper.settings")


class Environment(str, Enum):
    """Environment types"""
    DEVELOPMENT = "development"
    STAGING = "staging"
    PRODUCTION = "production"
    TESTING = "testing"


if PYDANTIC_AVAILABLE:
    class Settings(BaseSettings):
        """Application settings with validation"""
        
        # Environment
        environment: Environment = Field(
            default=Environment.DEVELOPMENT,
            env="ENVIRONMENT"
        )
        
        # API Keys
        openai_api_key: Optional[str] = Field(default=None, env="OPENAI_API_KEY")
        huggingface_api_key: Optional[str] = Field(default=None, env="HUGGINGFACE_API_KEY")
        
        # Logging
        log_level: str = Field(default="INFO", env="LOG_LEVEL")
        log_file: Optional[str] = Field(default=None, env="LOG_FILE")
        log_json: bool = Field(default=False, env="LOG_JSON")
        
        # Rate Limiting
        default_rate_limit: float = Field(default=10.0, env="DEFAULT_RATE_LIMIT")
        default_burst_limit: float = Field(default=20.0, env="DEFAULT_BURST_LIMIT")
        
        # Retry Configuration
        max_retries: int = Field(default=3, env="MAX_RETRIES")
        initial_retry_delay: float = Field(default=1.0, env="INITIAL_RETRY_DELAY")
        max_retry_delay: float = Field(default=60.0, env="MAX_RETRY_DELAY")
        retry_exponential_base: float = Field(default=2.0, env="RETRY_EXPONENTIAL_BASE")
        
        # Caching
        cache_enabled: bool = Field(default=True, env="CACHE_ENABLED")
        cache_ttl: int = Field(default=3600, env="CACHE_TTL")  # 1 hour
        cache_max_size: int = Field(default=1000, env="CACHE_MAX_SIZE")
        
        # Timeouts
        request_timeout: float = Field(default=120.0, env="REQUEST_TIMEOUT")
        
        # HuggingFace
        use_local_hf: bool = Field(default=False, env="USE_LOCAL_HF")
        hf_device: str = Field(default="auto", env="HF_DEVICE")
        
        @validator("log_level")
        def validate_log_level(cls, v):
            valid_levels = ["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"]
            if v.upper() not in valid_levels:
                raise ValueError(f"log_level must be one of {valid_levels}")
            return v.upper()
        
        @validator("hf_device")
        def validate_hf_device(cls, v):
            valid_devices = ["auto", "cpu", "cuda"]
            if v.lower() not in valid_devices:
                raise ValueError(f"hf_device must be one of {valid_devices}")
            return v.lower()
        
        class Config:
            env_file = ".env"
            env_file_encoding = "utf-8"
            case_sensitive = False
else:
    # Fallback implementation without pydantic
    class Settings:
        """Basic settings without validation"""
        
        def __init__(self):
            self.environment = Environment(os.getenv("ENVIRONMENT", "development"))
            self.openai_api_key = os.getenv("OPENAI_API_KEY")
            self.huggingface_api_key = os.getenv("HUGGINGFACE_API_KEY")
            self.log_level = os.getenv("LOG_LEVEL", "INFO")
            self.log_file = os.getenv("LOG_FILE")
            self.log_json = os.getenv("LOG_JSON", "false").lower() == "true"
            self.default_rate_limit = float(os.getenv("DEFAULT_RATE_LIMIT", "10.0"))
            self.default_burst_limit = float(os.getenv("DEFAULT_BURST_LIMIT", "20.0"))
            self.max_retries = int(os.getenv("MAX_RETRIES", "3"))
            self.initial_retry_delay = float(os.getenv("INITIAL_RETRY_DELAY", "1.0"))
            self.max_retry_delay = float(os.getenv("MAX_RETRY_DELAY", "60.0"))
            self.retry_exponential_base = float(os.getenv("RETRY_EXPONENTIAL_BASE", "2.0"))
            self.cache_enabled = os.getenv("CACHE_ENABLED", "true").lower() == "true"
            self.cache_ttl = int(os.getenv("CACHE_TTL", "3600"))
            self.cache_max_size = int(os.getenv("CACHE_MAX_SIZE", "1000"))
            self.request_timeout = float(os.getenv("REQUEST_TIMEOUT", "120.0"))
            self.use_local_hf = os.getenv("USE_LOCAL_HF", "false").lower() == "true"
            self.hf_device = os.getenv("HF_DEVICE", "auto").lower()
            
            if not PYDANTIC_AVAILABLE:
                logger.warning(
                    "pydantic not available. Using basic settings without validation. "
                    "Install pydantic for full validation support."
                )


# Global settings instance
_settings: Optional[Settings] = None


def get_settings() -> Settings:
    """Get or create settings instance"""
    global _settings
    if _settings is None:
        _settings = Settings()
    return _settings
