---
layout: default
title: API Reference
nav_order: 3
---

## API Reference

This document provides the **comprehensive API reference** for the Chatbot API Wrapper, including object structure, method signatures, expected parameters, return types, example usages, error modes, and supported features/providers.

---

## ChatbotWrapper

Primary wrapper class for working with both HuggingFace and OpenAI models in a unified fashion.

### Initialization

```python
ChatbotWrapper(
    huggingface_api_key: Optional[str] = None,
    openai_api_key: Optional[str] = None,
    use_local_hf: bool = False,
    hf_device: str = "auto"
)
```

**Arguments:**

- **huggingface_api_key** (*str, optional*): API key for HuggingFace. Required for HuggingFace hosted model calls.
- **openai_api_key** (*str, optional*): API key for OpenAI. Required for OpenAI model calls.
- **use_local_hf** (*bool*): If `True`, loads compatible HuggingFace models locally (requires compatible files and hardware).
- **hf_device** (*str*): Device identifier for running local HF models (`"cpu"`, `"cuda"`, or `"auto"`).

**Quick example:**

```python
from api_wrapper import ChatbotWrapper

wrapper = ChatbotWrapper(
    huggingface_api_key="hf_...",
    openai_api_key="sk-...",
    use_local_hf=True,   # True if you want to use local HuggingFace models (must be downloaded)
    hf_device="cuda"     # "cuda", "cpu", or "auto"
)
```

---

## Methods

### chat()

Return a single response from a given model.

```python
chat(
    model: str,
    messages: Union[str, List[Dict[str, str]]],
    provider: Union['Provider', str] = Provider.AUTO,
    temperature: float = 0.7,
    max_tokens: int = 512,
    **kwargs
) -> Dict[str, Any]
```

**Parameters:**

- **model** (*str*): Model name (e.g. `"gpt-3.5-turbo"`, `"mistralai/Mistral-7B-Instruct-v0.2"`)
- **messages** (*str or List\[Dict\[str, str\]\]*): Message or list of dicts with `role` and `content`.
- **provider** (*Provider or str*): `"huggingface"`, `"openai"`, or `Provider.AUTO` (default: `AUTO`; auto-detects from model name).
- **temperature** (*float*): Sampling temperature [0.0, 2.0].
- **max_tokens** (*int*): Max tokens to generate.
- **\*\*kwargs**: Model/provider-specific arguments (see below).

**Returns (`dict`):**

- `response` (*str*): Generated reply.
- `model` (*str*): Model name.
- `provider` (*str*): Provider used.
- `usage` (*dict, OpenAI only*): Token usage statistics (if available).
- `finish_reason` (*str, OpenAI only*): Why the generation stopped (if available).
- `method` (*str, HuggingFace only*): `"api"` or `"local"` (present if using HuggingFace).

**Basic example:**

```python
response = wrapper.chat(
    model="gpt-3.5-turbo",
    messages="Hello!",
    temperature=0.7,
    max_tokens=100
)
print(response["response"])
```

---

### stream_chat()

**Stream** the generation output token-by-token or chunk-by-chunk.

```python
stream_chat(
    model: str,
    messages: Union[str, List[Dict[str, str]]],
    provider: Union['Provider', str] = Provider.AUTO,
    temperature: float = 0.7,
    max_tokens: int = 512,
    **kwargs
) -> Iterator[str]
```

- Parameters: Same as `chat()`.
- Returns: Iterator of response chunk strings (yielded as soon as produced).

**Example:**

```python
for chunk in wrapper.stream_chat(
    model="gpt-3.5-turbo",
    messages="Tell me a story"
):
    print(chunk, end='', flush=True)
print("[DONE]")
```

---

### list_models()

List all available models from the configured providers.

```python
list_models(provider: Optional[Union['Provider', str]] = None) -> Dict[str, List[str]]
```

- **provider** (*str or Provider, optional*): `"huggingface"`, `"openai"`, or `None` (lists all).
- **Returns** (`dict`): Keys `"huggingface"` and/or `"openai"` mapping to lists of available model names.

**Example:**

```python
models = wrapper.list_models()
print("OpenAI models:", models["openai"])
```

---

### get_model_info()

Return full metadata for a specified model, if available.

```python
get_model_info(model: str) -> Dict[str, Any]
```

**Arguments:**

- **model** (*str*): Name of the model.

**Returns** (`dict`): Contains at least:

- `name` (*str*): Model name.
- `provider` (*str*): Provider name.
- `description` (*str*): Description, if available.

**Example:**

```python
info = wrapper.get_model_info("gpt-3.5-turbo")
print(info["description"])
```

---

### conversation()

Start a persistent multi-turn conversation context.

```python
conversation(
    model: str,
    system_prompt: Optional[str] = None,
    provider: Union['Provider', str] = Provider.AUTO,
    temperature: float = 0.7,
    max_tokens: int = 512,
    **kwargs
) -> Conversation
```

- Arguments as above (`model`, `system_prompt`, etc.).
- Returns: `Conversation` instance (see below).

**Example:**

```python
conv = wrapper.conversation(
    model="gpt-3.5-turbo",
    system_prompt="You are a helpful assistant.",
    temperature=0.7,
)
```

---

## Conversation Class

Tracks message history and encapsulates multi-turn chat.

### Conversation Methods

#### send(message: str) -> str

Send a message and append to the conversation. Returns next assistant reply.

```python
response = conv.send("What is Python?")
print(response)
```

#### stream_send(message: str) -> Iterator[str]

Send a message and **stream** the assistant response.

```python
for chunk in conv.stream_send("Summarize the Industrial Revolution."):
    print(chunk, end='', flush=True)
```

#### reset() -> None

Reset conversation **history** (retains system prompt).

```python
conv.reset()
```

#### get_history() -> List[Dict[str, str]]

Retrieve full conversation history as a list of dicts with `"role"` and `"content"`.

```python
history = conv.get_history()
for msg in history:
    print(f"{msg['role']}: {msg['content']}")
```

---

## HuggingFaceClient

Direct interface for HuggingFace models (skip wrapper).

### HuggingFaceClient Initialization

```python
HuggingFaceClient(
    api_key: Optional[str] = None,
    use_local: bool = False,
    device: str = "auto"
)
```

- **api_key** (*str, optional*): HuggingFace API token.
- **use_local** (*bool*): Use local models if `True`.
- **device** (*str*): Device for local inference.

### HuggingFaceClient Methods

- **chat()**: Same as wrapper.
- **stream_chat()**: Streaming responses.
- **list_available_models()**: List loaded/configured models.

---

## OpenAIClient

Direct interface to OpenAI REST API.

### OpenAIClient Initialization

```python
OpenAIClient(
    api_key: Optional[str] = None,
    base_url: Optional[str] = None  # Optional custom API endpoint
)
```

- **api_key** (*str, optional*): OpenAI API key.
- **base_url** (*str, optional*): Custom API endpoint.

### OpenAIClient Methods

- **chat()**: Generate response.
- **stream_chat()**: Streaming responses.
- **list_available_models()**: List accessible models for API key.
- **get_model_info()**: Return metadata for a model.

---

## Provider Enum

Provider identifier used for dispatching requests.

```python
from api_wrapper import Provider

Provider.HUGGINGFACE  # (or "huggingface")
Provider.OPENAI       # (or "openai")
Provider.AUTO         # (auto-detect from model name)
```

---

## Message Format

### String

Just a single prompt message:

```python
messages = "Hello, how are you?"
```

### List-of-Dicts

Structured multi-turn conversation. Each dict **must** have keys `'role'` and `'content'`. Typical roles:

- `"system"`: Initial instruction/context.
- `"user"`: User input.
- `"assistant"`: Model/assistant output.

```python
messages = [
    {"role": "system", "content": "You are a helpful assistant."},
    {"role": "user", "content": "What is Python?"},
    {"role": "assistant", "content": "Python is a programming language."},
    {"role": "user", "content": "Tell me more."},
]
```

---

## Error Handling

All methods may raise Python exceptions for API, connection, or input errors.

**Common exceptions:**

- **ValueError**: Invalid parameters; e.g., missing required API key or invalid model/provider.
- **Exception**: Covers other runtime or HTTP errors.

**Example:**

```python
try:
    response = wrapper.chat(model="invalid-model", messages="hi")
except ValueError as e:
    print("Chatbot error:", e)
except Exception as err:
    print("API failure:", err)
```

---

## Provider-Specific Parameters

Both OpenAI and HuggingFace support model-specific tuning parameters (passable as kwargs).

### OpenAI (add as kwargs)

- **frequency_penalty**: *float*, [-2.0, 2.0]
- **presence_penalty**: *float*, [-2.0, 2.0]
- **top_p**: *float*, [0.0, 1.0]
- **other OpenAI API parameters**...

```python
response = wrapper.chat(
    model="gpt-3.5-turbo",
    messages="test",
    frequency_penalty=0.0,
    presence_penalty=0.0,
    top_p=0.9,
)
```

### HuggingFace (add as kwargs)

- **top_p**: *float*
- **top_k**: *int*
- **repetition_penalty**: *float*
- **other supported HF API/generation parameters**...

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

### Models Registry

The Chatbot API Wrapper includes a comprehensive **Models Registry** (`models/models_registry.py`) with detailed information about all supported models, including:

- Full API endpoints and access methods
- Model specifications (parameters, context windows, architecture)
- Licensing information
- Cost information and free tier availability
- Recommended use cases and limitations
- Documentation links

**Access the Models Registry:**

```python
from models.models_registry import (
    get_model_info,
    list_models_by_provider,
    search_models,
    get_free_models,
    get_local_models,
)

# Get detailed model information
model_info = get_model_info("gpt-3.5-turbo")
print(f"Context Window: {model_info.specs.context_window}")
print(f"API Endpoint: {model_info.api_endpoint.url}")

# Search for models
results = search_models("instruction")

# Find free tier models
free_models = get_free_models()

# Find models that can run locally
local_models = get_local_models()
```

**Using the CLI script:**

```bash
python scripts/list-models.py list                    # List all models
python scripts/list-models.py provider huggingface    # List by provider
python scripts/list-models.py free                    # List free tier models
python scripts/list-models.py info gpt-3.5-turbo      # Show model details
python scripts/list-models.py search instruction      # Search models
```

The `ChatbotWrapper.get_model_info()` method automatically uses the models registry when available, providing comprehensive information instead of basic config data.

### OpenAI Models

- `gpt-4` - Most capable model
- `gpt-4-turbo` - Faster and more capable GPT-4 variant (128K context)
- `gpt-4-turbo-preview` - Preview version of GPT-4 Turbo
- `gpt-4o` - Latest multimodal model optimized for speed and cost
- `gpt-4o-mini` - Smaller, faster, more affordable GPT-4o
- `gpt-3.5-turbo` - Fast and efficient (16K context)
- `gpt-3.5-turbo-16k` - Extended context window

### HuggingFace Models

- `meta-llama/Llama-2-7b-chat-hf` - Llama 2 7B chat model
- `meta-llama/Llama-2-13b-chat-hf` - Llama 2 13B chat model
- `meta-llama/Meta-Llama-3-8B-Instruct` - Llama 3 8B instruction model
- `mistralai/Mistral-7B-Instruct-v0.2` - Mistral 7B instruction model
- `mistralai/Mixtral-8x7B-Instruct-v0.1` - Mixtral 8x7B mixture of experts
- `microsoft/DialoGPT-large` - Microsoft's conversational AI
- `google/flan-t5-xxl` - Google's instruction-tuned T5 model
- `google/gemma-7b-it` - Google's Gemma 7B instruction model
- `HuggingFaceH4/zephyr-7b-beta` - HuggingFace's Zephyr instruction model
- `Qwen/Qwen2.5-7B-Instruct` - Alibaba's Qwen 2.5 7B instruction model

*(For a full up-to-date list with detailed information, use `wrapper.list_models()` or the models registry.)*

---

## Return Value Examples

### OpenAI

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

### HuggingFace

```python
{
    "response": "Hello! How can I help you?",
    "model": "mistralai/Mistral-7B-Instruct-v0.2",
    "provider": "huggingface",
    "method": "api"  # Either "api" or "local"
}
```

---

**Tip:** If you find a missing API feature, method, or parameter, please [open an issue or contribute](../CONTRIBUTING.md).
