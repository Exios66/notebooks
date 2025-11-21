"""
Security utilities for input validation and sanitization
"""

import re
from typing import Union, List, Dict, Any, Optional

from .logger import get_logger
from .exceptions import ValidationError

logger = get_logger("api_wrapper.security")


# Maximum message length (in characters)
MAX_MESSAGE_LENGTH = 100000
MAX_MESSAGES_COUNT = 100


def validate_message(message: Union[str, Dict[str, str]]) -> str:
    """
    Validate and sanitize a single message

    Args:
        message: Message string or dict with 'content' key

    Returns:
        Validated message content

    Raises:
        ValidationError if message is invalid
    """
    if isinstance(message, dict):
        if "content" not in message:
            raise ValidationError(
                "Message dict must contain 'content' key",
                field="content"
            )
        content = message["content"]
    elif isinstance(message, str):
        content = message
    else:
        raise ValidationError(
            f"Message must be str or dict, got {type(message).__name__}",
            field="message"
        )

    if not isinstance(content, str):
        raise ValidationError(
            "Message content must be a string",
            field="content"
        )

    if len(content) > MAX_MESSAGE_LENGTH:
        raise ValidationError(
            f"Message too long (max {MAX_MESSAGE_LENGTH} characters)",
            field="content"
        )

    if len(content.strip()) == 0:
        raise ValidationError(
            "Message content cannot be empty",
            field="content"
        )

    return content


def validate_messages(messages: Union[str, List[Dict[str, str]]]) -> List[Dict[str, str]]:
    """
    Validate and normalize messages

    Args:
        messages: Single message string or list of message dicts

    Returns:
        List of validated message dicts

    Raises:
        ValidationError if messages are invalid
    """
    if isinstance(messages, str):
        return [{"role": "user", "content": validate_message(messages)}]

    if not isinstance(messages, list):
        raise ValidationError(
            f"Messages must be str or list, got {type(messages).__name__}",
            field="messages"
        )

    if len(messages) > MAX_MESSAGES_COUNT:
        raise ValidationError(
            f"Too many messages (max {MAX_MESSAGES_COUNT})",
            field="messages"
        )

    validated = []
    for i, msg in enumerate(messages):
        if not isinstance(msg, dict):
            raise ValidationError(
                f"Message {i} must be a dict",
                field=f"messages[{i}]"
            )

        if "role" not in msg:
            raise ValidationError(
                f"Message {i} missing 'role' field",
                field=f"messages[{i}].role"
            )

        role = msg["role"]
        if role not in ["system", "user", "assistant"]:
            raise ValidationError(
                f"Invalid role '{role}' in message {i} (must be 'system', 'user', or 'assistant')",
                field=f"messages[{i}].role"
            )

        content = validate_message(msg)
        validated.append({"role": role, "content": content})

    return validated


def validate_model_name(model: str) -> str:
    """
    Validate model name

    Args:
        model: Model identifier

    Returns:
        Validated model name

    Raises:
        ValidationError if model name is invalid
    """
    if not isinstance(model, str):
        raise ValidationError(
            f"Model must be a string, got {type(model).__name__}",
            field="model"
        )

    if len(model.strip()) == 0:
        raise ValidationError(
            "Model name cannot be empty",
            field="model"
        )

    if len(model) > 200:
        raise ValidationError(
            "Model name too long (max 200 characters)",
            field="model"
        )

    # Check for potentially dangerous characters
    if re.search(r'[<>"\']', model):
        raise ValidationError(
            "Model name contains invalid characters",
            field="model"
        )

    return model.strip()


def validate_temperature(temperature: float) -> float:
    """
    Validate temperature parameter

    Args:
        temperature: Temperature value

    Returns:
        Validated temperature

    Raises:
        ValidationError if temperature is invalid
    """
    if not isinstance(temperature, (int, float)):
        raise ValidationError(
            f"Temperature must be a number, got {type(temperature).__name__}",
            field="temperature"
        )

    if temperature < 0.0 or temperature > 2.0:
        raise ValidationError(
            "Temperature must be between 0.0 and 2.0",
            field="temperature"
        )

    return float(temperature)


def validate_max_tokens(max_tokens: int) -> int:
    """
    Validate max_tokens parameter

    Args:
        max_tokens: Maximum tokens value

    Returns:
        Validated max_tokens

    Raises:
        ValidationError if max_tokens is invalid
    """
    if not isinstance(max_tokens, int):
        raise ValidationError(
            f"max_tokens must be an integer, got {type(max_tokens).__name__}",
            field="max_tokens"
        )

    if max_tokens < 1:
        raise ValidationError(
            "max_tokens must be at least 1",
            field="max_tokens"
        )

    if max_tokens > 100000:
        raise ValidationError(
            "max_tokens too large (max 100000)",
            field="max_tokens"
        )

    return max_tokens


def sanitize_for_logging(data: Any) -> Any:
    """
    Sanitize data for logging (remove sensitive information)

    Args:
        data: Data to sanitize

    Returns:
        Sanitized data
    """
    if isinstance(data, dict):
        sanitized = {}
        for key, value in data.items():
            key_lower = key.lower()
            if any(sensitive in key_lower for sensitive in [
                "key", "token", "password", "secret", "auth", "credential"
            ]):
                sanitized[key] = "***REDACTED***"
            else:
                sanitized[key] = sanitize_for_logging(value)
        return sanitized
    elif isinstance(data, list):
        return [sanitize_for_logging(item) for item in data]
    elif isinstance(data, str):
        # Check if string looks like an API key
        if len(data) > 20 and any(char in data for char in ["sk-", "hf_", "xoxb-"]):
            return "***REDACTED***"
        return data
    else:
        return data


def mask_api_key(api_key: Optional[str]) -> str:
    """
    Mask API key for logging

    Args:
        api_key: API key to mask

    Returns:
        Masked API key
    """
    if not api_key:
        return "None"

    if len(api_key) <= 8:
        return "***"

    return api_key[:4] + "***" + api_key[-4:]


def validate_request_size(messages: Union[str, List[Dict[str, str]]]) -> int:
    """
    Validate and calculate request size

    Args:
        messages: Messages to validate

    Returns:
        Total character count

    Raises:
        ValidationError if request is too large
    """
    validated = validate_messages(messages)
    total_size = sum(len(msg["content"]) for msg in validated)

    if total_size > MAX_MESSAGE_LENGTH * MAX_MESSAGES_COUNT:
        raise ValidationError(
            f"Request too large (max {MAX_MESSAGE_LENGTH * MAX_MESSAGES_COUNT} characters)",
            field="messages"
        )

    return total_size
