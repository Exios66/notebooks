---
layout: default
title: API Endpoints
nav_order: 5
---

# API Endpoints Reference

Complete reference for all API endpoints and their usage.

## Overview

The Chatbot API Wrapper provides programmatic access to chatbot models through Python classes and methods. This document describes all available endpoints (methods) and their parameters.

## ChatbotWrapper Endpoints

### Initialization

**Endpoint:** `ChatbotWrapper()`

**Description:** Initialize the main wrapper class.

**Parameters:**
- `huggingface_api_key` (str, optional): HuggingFace API key
- `openai_api_key` (str, optional): OpenAI API key  
- `use_local_hf` (bool, default: False): Use local HuggingFace models
- `hf_device` (str, default: "auto"): Device for local models

**Returns:** `ChatbotWrapper` instance

**Example:**
```python
wrapper = ChatbotWrapper(
    openai_api_key="sk-...",
    huggingface_api_key="hf_...",
    use_local_hf=False
)
```

---

### chat()

**Endpoint:** `wrapper.chat()`

**Description:** Generate a chat response from a model.

**Method Signature:**
```python
chat(
    model: str,
    messages: Union[str, List[Dict[str, str]]],
    provider: Union[Provider, str] = Provider.AUTO,
    temperature: float = 0.7,
    max_tokens: int = 512,
    **kwargs
) -> Dict[str, Any]
```

**Parameters:**

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `model` | str | Yes | - | Model identifier |
| `messages` | str \| List[Dict] | Yes | - | Message(s) to send |
| `provider` | str | No | "auto" | Provider ("openai", "huggingface", "auto") |
| `temperature` | float | No | 0.7 | Sampling temperature (0.0-2.0) |
| `max_tokens` | int | No | 512 | Maximum tokens to generate |
| `**kwargs` | dict | No | - | Provider-specific parameters |

**Returns:**
```python
{
    "response": str,           # Generated text
    "model": str,              # Model used
    "provider": str,           # Provider name
    "usage": dict,             # Token usage (OpenAI only)
    "finish_reason": str       # Finish reason (OpenAI only)
}
```

**Example:**
```python
response = wrapper.chat(
    model="gpt-3.5-turbo",
    messages="Hello!",
    temperature=0.7,
    max_tokens=100
)
```

**Error Responses:**
- `ValueError`: Invalid parameters or missing API keys
- `Exception`: API request failures

---

### stream_chat()

**Endpoint:** `wrapper.stream_chat()`

**Description:** Stream chat responses in real-time.

**Method Signature:**
```python
stream_chat(
    model: str,
    messages: Union[str, List[Dict[str, str]]],
    provider: Union[Provider, str] = Provider.AUTO,
    temperature: float = 0.7,
    max_tokens: int = 512,
    **kwargs
) -> Iterator[str]
```

**Parameters:** Same as `chat()`

**Returns:** Iterator yielding response chunks (str)

**Example:**
```python
for chunk in wrapper.stream_chat(
    model="gpt-3.5-turbo",
    messages="Tell me a story"
):
    print(chunk, end='', flush=True)
```

---

### list_models()

**Endpoint:** `wrapper.list_models()`

**Description:** List available models for specified provider(s).

**Method Signature:**
```python
list_models(provider: Optional[Union[Provider, str]] = None) -> Dict[str, List[str]]
```

**Parameters:**

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `provider` | str | No | None | Provider name or None for all |

**Returns:**
```python
{
    "huggingface": ["model1", "model2", ...],
    "openai": ["gpt-4", "gpt-3.5-turbo", ...]
}
```

**Example:**
```python
models = wrapper.list_models()
openai_models = wrapper.list_models(provider="openai")
```

---

### get_model_info()

**Endpoint:** `wrapper.get_model_info()`

**Description:** Get information about a specific model.

**Method Signature:**
```python
get_model_info(model: str) -> Dict[str, Any]
```

**Parameters:**

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `model` | str | Yes | Model identifier |

**Returns:**
```python
{
    "name": str,
    "provider": str,
    "description": str,
    ...
}
```

**Example:**
```python
info = wrapper.get_model_info("gpt-3.5-turbo")
```

---

### conversation()

**Endpoint:** `wrapper.conversation()`

**Description:** Create a conversation context for multi-turn interactions.

**Method Signature:**
```python
conversation(
    model: str,
    system_prompt: Optional[str] = None,
    provider: Union[Provider, str] = Provider.AUTO,
    temperature: float = 0.7,
    max_tokens: int = 512,
    **kwargs
) -> Conversation
```

**Parameters:**

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `model` | str | Yes | - | Model identifier |
| `system_prompt` | str | No | None | System prompt |
| `provider` | str | No | "auto" | Provider |
| `temperature` | float | No | 0.7 | Temperature |
| `max_tokens` | int | No | 512 | Max tokens |
| `**kwargs` | dict | No | - | Additional params |

**Returns:** `Conversation` instance

**Example:**
```python
conv = wrapper.conversation(
    model="gpt-3.5-turbo",
    system_prompt="You are helpful.",
    temperature=0.7
)
```

---

## Conversation Endpoints

### send()

**Endpoint:** `conv.send()`

**Description:** Send a message and get response.

**Method Signature:**
```python
send(message: str) -> str
```

**Parameters:**

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `message` | str | Yes | User message |

**Returns:** Assistant response (str)

**Example:**
```python
response = conv.send("What is Python?")
```

---

### stream_send()

**Endpoint:** `conv.stream_send()`

**Description:** Send a message and stream response.

**Method Signature:**
```python
stream_send(message: str) -> Iterator[str]
```

**Parameters:** Same as `send()`

**Returns:** Iterator yielding response chunks

**Example:**
```python
for chunk in conv.stream_send("Tell me a story"):
    print(chunk, end='', flush=True)
```

---

### reset()

**Endpoint:** `conv.reset()`

**Description:** Reset conversation history (keeps system prompt).

**Method Signature:**
```python
reset() -> None
```

**Parameters:** None

**Returns:** None

**Example:**
```python
conv.reset()
```

---

### get_history()

**Endpoint:** `conv.get_history()`

**Description:** Get conversation history.

**Method Signature:**
```python
get_history() -> List[Dict[str, str]]
```

**Parameters:** None

**Returns:** List of message dictionaries

**Example:**
```python
history = conv.get_history()
```

---

## HuggingFaceClient Endpoints

### Initialization

**Endpoint:** `HuggingFaceClient()`

**Parameters:**
- `api_key` (str, optional): HuggingFace API key
- `use_local` (bool, default: False): Use local models
- `device` (str, default: "auto"): Device ("cpu", "cuda", "auto")

### Methods

- `chat()`: Same interface as wrapper
- `stream_chat()`: Stream responses
- `list_available_models()`: List configured models

---

## OpenAIClient Endpoints

### Initialization

**Endpoint:** `OpenAIClient()`

**Parameters:**
- `api_key` (str, optional): OpenAI API key
- `base_url` (str, optional): Custom base URL

### Methods

- `chat()`: Generate response
- `stream_chat()`: Stream responses
- `list_available_models()`: List OpenAI models
- `get_model_info()`: Get model information

---

## Provider-Specific Parameters

### OpenAI Parameters

```python
{
    "frequency_penalty": float,  # -2.0 to 2.0
    "presence_penalty": float,  # -2.0 to 2.0
    "top_p": float,             # 0.0 to 1.0
    "n": int,                   # Number of completions
    "stop": List[str]           # Stop sequences
}
```

### HuggingFace Parameters

```python
{
    "top_p": float,             # Nucleus sampling
    "top_k": int,               # Top-k sampling
    "repetition_penalty": float, # Repetition penalty
    "do_sample": bool,          # Enable sampling
    "return_full_text": bool    # Return full text
}
```

---

## Response Formats

### OpenAI Response

```json
{
    "response": "Hello! How can I help?",
    "model": "gpt-3.5-turbo",
    "provider": "openai",
    "usage": {
        "prompt_tokens": 10,
        "completion_tokens": 8,
        "total_tokens": 18
    },
    "finish_reason": "stop"
}
```

### HuggingFace Response

```json
{
    "response": "Hello! How can I help?",
    "model": "mistralai/Mistral-7B-Instruct-v0.2",
    "provider": "huggingface",
    "method": "api"
}
```

---

## Error Handling

### Common Error Types

**ValueError**
- Missing API keys
- Invalid model names
- Invalid parameter values

**Exception**
- API request failures
- Network errors
- Model loading errors

### Error Response Format

```python
{
    "error": "Error message",
    "type": "ValueError" | "Exception"
}
```

---

## Rate Limits

### OpenAI
- Varies by model and tier
- Check OpenAI documentation for current limits

### HuggingFace
- Free tier: Limited requests
- Pro tier: Higher limits
- Check HuggingFace documentation

---

## Best Practices

1. **API Keys**: Store in environment variables
2. **Error Handling**: Always wrap calls in try-except
3. **Rate Limits**: Implement retry logic with backoff
4. **Token Usage**: Monitor usage for cost control
5. **Caching**: Cache responses when appropriate

---

## Quick Reference

| Endpoint | Method | Returns |
|----------|--------|---------|
| `ChatbotWrapper()` | Constructor | Wrapper instance |
| `chat()` | POST | Dict with response |
| `stream_chat()` | POST | Iterator[str] |
| `list_models()` | GET | Dict[str, List[str]] |
| `get_model_info()` | GET | Dict[str, Any] |
| `conversation()` | Constructor | Conversation instance |
| `conv.send()` | POST | str |
| `conv.stream_send()` | POST | Iterator[str] |
| `conv.reset()` | POST | None |
| `conv.get_history()` | GET | List[Dict] |

