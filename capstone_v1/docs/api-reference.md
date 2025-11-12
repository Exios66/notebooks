---
layout: default
title: API Reference
nav_order: 3
---

# API Reference

Complete API documentation for the Chatbot API Wrapper.

## ChatbotWrapper

Main wrapper class for chatbot interactions.

### Initialization

```python
ChatbotWrapper(
    huggingface_api_key: Optional[str] = None,
    openai_api_key: Optional[str] = None,
    use_local_hf: bool = False,
    hf_device: str = "auto"
)
```

**Parameters:**

- `huggingface_api_key` (str, optional): HuggingFace API key
- `openai_api_key` (str, optional): OpenAI API key
- `use_local_hf` (bool): Use local HuggingFace models instead of API
- `hf_device` (str): Device for local models ('cpu', 'cuda', 'auto')

**Example:**

```python
wrapper = ChatbotWrapper(
    openai_api_key="sk-...",
    huggingface_api_key="hf_...",
    use_local_hf=False,
    hf_device="auto"
)
```

---

## Methods

### chat()

Generate a chat response.

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

- `model` (str): Model identifier (e.g., 'gpt-3.5-turbo', 'mistralai/Mistral-7B-Instruct-v0.2')
- `messages` (str | List[Dict]): Message string or list of message dicts with 'role' and 'content'
- `provider` (str): Provider to use ('huggingface', 'openai', 'auto')
- `temperature` (float): Sampling temperature (0.0 to 2.0)
- `max_tokens` (int): Maximum tokens to generate
- `**kwargs`: Additional provider-specific parameters

**Returns:**

```python
{
    "response": str,           # Generated response text
    "model": str,              # Model identifier
    "provider": str,           # Provider name
    "usage": dict,             # Token usage (OpenAI only)
    "finish_reason": str,      # Finish reason (OpenAI only)
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

---

### stream_chat()

Stream chat responses in real-time.

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

List available models for specified provider(s).

```python
list_models(provider: Optional[Union[Provider, str]] = None) -> Dict[str, List[str]]
```

**Parameters:**

- `provider` (str, optional): Provider to list ('huggingface', 'openai', or None for all)

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
print(models["openai"])
```

---

### get_model_info()

Get information about a specific model.

```python
get_model_info(model: str) -> Dict[str, Any]
```

**Parameters:**

- `model` (str): Model identifier

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
print(info["description"])
```

---

### conversation()

Create a conversation context for multi-turn interactions.

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

- `model` (str): Model identifier
- `system_prompt` (str, optional): System prompt to set context
- `provider` (str): Provider to use
- `temperature` (float): Sampling temperature
- `max_tokens` (int): Maximum tokens per response
- `**kwargs`: Additional parameters

**Returns:** `Conversation` object

**Example:**

```python
conv = wrapper.conversation(
    model="gpt-3.5-turbo",
    system_prompt="You are a helpful assistant.",
    temperature=0.7
)
```

---

## Conversation Class

Manages multi-turn conversation context.

### Methods

#### send()

Send a message and get response.

```python
send(message: str) -> str
```

**Parameters:**

- `message` (str): User message

**Returns:** Assistant response (str)

**Example:**

```python
response = conv.send("What is Python?")
```

#### stream_send()

Send a message and stream response.

```python
stream_send(message: str) -> Iterator[str]
```

**Parameters:**

- `message` (str): User message

**Returns:** Iterator yielding response chunks

**Example:**

```python
for chunk in conv.stream_send("Tell me a story"):
    print(chunk, end='', flush=True)
```

#### reset()

Reset conversation history (keeps system prompt).

```python
reset() -> None
```

**Example:**

```python
conv.reset()
```

#### get_history()

Get conversation history.

```python
get_history() -> List[Dict[str, str]]
```

**Returns:** List of message dictionaries

**Example:**

```python
history = conv.get_history()
for msg in history:
    print(f"{msg['role']}: {msg['content']}")
```

---

## HuggingFaceClient

Direct client for HuggingFace models.

### Initialization

```python
HuggingFaceClient(
    api_key: Optional[str] = None,
    use_local: bool = False,
    device: str = "auto"
)
```

### Methods

- `chat()`: Generate response (same interface as wrapper)
- `stream_chat()`: Stream responses
- `list_available_models()`: List configured models

---

## OpenAIClient

Direct client for OpenAI models.

### Initialization

```python
OpenAIClient(
    api_key: Optional[str] = None,
    base_url: Optional[str] = None
)
```

### Methods

- `chat()`: Generate response
- `stream_chat()`: Stream responses
- `list_available_models()`: List OpenAI models
- `get_model_info()`: Get model information

---

## Provider Enum

Provider selection enum.

```python
from api_wrapper import Provider

Provider.HUGGINGFACE  # HuggingFace provider
Provider.OPENAI       # OpenAI provider
Provider.AUTO         # Auto-detect from model name
```

---

## Message Format

### String Format

Simple string message:

```python
messages = "Hello, how are you?"
```

### List Format

List of message dictionaries:

```python
messages = [
    {"role": "system", "content": "You are a helpful assistant."},
    {"role": "user", "content": "What is Python?"},
    {"role": "assistant", "content": "Python is a programming language."},
    {"role": "user", "content": "Tell me more."},
]
```

**Roles:**

- `system`: System prompt (optional, typically first message)
- `user`: User messages
- `assistant`: Assistant responses (for context)

---

## Error Handling

### Common Exceptions

**ValueError**: Invalid parameters or missing API keys

```python
try:
    wrapper.chat(model="invalid", messages="test")
except ValueError as e:
    print(f"Error: {e}")
```

**Exception**: API request failures

```python
try:
    response = wrapper.chat(model="gpt-3.5-turbo", messages="test")
except Exception as e:
    print(f"API Error: {e}")
```

---

## Provider-Specific Parameters

### OpenAI Parameters

```python
response = wrapper.chat(
    model="gpt-3.5-turbo",
    messages="test",
    frequency_penalty=0.0,  # -2.0 to 2.0
    presence_penalty=0.0,   # -2.0 to 2.0
    top_p=0.9,
)
```

### HuggingFace Parameters

```python
response = wrapper.chat(
    model="mistralai/Mistral-7B-Instruct-v0.2",
    messages="test",
    top_p=0.9,
    top_k=50,
    repetition_penalty=1.1,
)
```

---

## Available Models

### OpenAI Models

- `gpt-4`: Most capable model
- `gpt-4-turbo`: Faster GPT-4 variant
- `gpt-4-turbo-preview`: Preview version
- `gpt-3.5-turbo`: Fast and efficient
- `gpt-3.5-turbo-16k`: Extended context

### HuggingFace Models

- `meta-llama/Llama-2-7b-chat-hf`: Llama 2 7B
- `meta-llama/Llama-2-13b-chat-hf`: Llama 2 13B
- `meta-llama/Meta-Llama-3-8B-Instruct`: Llama 3 8B
- `mistralai/Mistral-7B-Instruct-v0.2`: Mistral 7B
- `microsoft/DialoGPT-large`: DialoGPT
- `google/flan-t5-xxl`: FLAN-T5
- `HuggingFaceH4/zephyr-7b-beta`: Zephyr 7B

---

## Return Value Examples

### OpenAI Response

```python
{
    "response": "Hello! How can I help you?",
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

```python
{
    "response": "Hello! How can I help you?",
    "model": "mistralai/Mistral-7B-Instruct-v0.2",
    "provider": "huggingface",
    "method": "api"  # or "local"
}
```
