# Chatbot API Wrapper

A comprehensive Python wrapper for interacting with chatbot models from HuggingFace and OpenAI. This wrapper provides a unified interface for using various specialized chatbot models from both platforms.

## Features

- **Unified Interface**: Single API for both HuggingFace and OpenAI models
- **Multiple Providers**: Support for HuggingFace Inference API, local HuggingFace models, and OpenAI API
- **Specialized Models**: Pre-configured with popular chatbot models from both platforms
- **Streaming Support**: Real-time streaming responses for better user experience
- **Conversation Management**: Built-in conversation context for multi-turn interactions
- **Flexible Configuration**: Easy to configure and extend with new models

## Installation

1. Install dependencies:

```bash
pip install -r requirements.txt
```

2. Set up API keys (optional, can also pass directly):

```bash
export OPENAI_API_KEY="your-openai-api-key"
export HUGGINGFACE_API_KEY="your-huggingface-api-key"
```

## Quick Start

### Basic Usage

```python
from api_wrapper import ChatbotWrapper

# Initialize wrapper
wrapper = ChatbotWrapper(
    openai_api_key="your-key",  # Optional if set as env var
    huggingface_api_key="your-key",  # Optional if set as env var
)

# Simple chat
response = wrapper.chat(
    model="gpt-3.5-turbo",
    messages="Hello, how are you?",
    temperature=0.7,
)
print(response['response'])
```

### Multi-turn Conversation

```python
# Create a conversation context
conv = wrapper.conversation(
    model="gpt-3.5-turbo",
    system_prompt="You are a helpful assistant.",
)

# Send messages
response1 = conv.send("What is Python?")
response2 = conv.send("Can you give me an example?")
```

### Streaming Responses

```python
# Stream responses in real-time
for chunk in wrapper.stream_chat(
    model="gpt-3.5-turbo",
    messages="Tell me a story",
):
    print(chunk, end='', flush=True)
```

### Using HuggingFace Models

```python
# Via Inference API
response = wrapper.chat(
    model="mistralai/Mistral-7B-Instruct-v0.2",
    messages="Explain machine learning",
    provider="huggingface",
)

# Or use local models
wrapper = ChatbotWrapper(use_local_hf=True, hf_device="cuda")
response = wrapper.chat(
    model="microsoft/DialoGPT-large",
    messages="Hello!",
)
```

## Available Models

### OpenAI Models

- `gpt-4`: Most capable model
- `gpt-4-turbo`: Faster GPT-4 variant
- `gpt-3.5-turbo`: Fast and efficient
- `gpt-3.5-turbo-16k`: Extended context window

### HuggingFace Models

- `meta-llama/Llama-2-7b-chat-hf`: Llama 2 7B chat model
- `meta-llama/Llama-2-13b-chat-hf`: Llama 2 13B chat model
- `mistralai/Mistral-7B-Instruct-v0.2`: Mistral 7B instruction model
- `microsoft/DialoGPT-large`: Microsoft's conversational AI
- `google/flan-t5-xxl`: Google's instruction-tuned T5
- `HuggingFaceH4/zephyr-7b-beta`: Zephyr instruction model
- `meta-llama/Meta-Llama-3-8B-Instruct`: Llama 3 8B instruction model

## API Reference

### ChatbotWrapper

Main wrapper class for chatbot interactions.

#### Methods

- `chat(model, messages, provider='auto', temperature=0.7, max_tokens=512, **kwargs)`: Generate a chat response
- `stream_chat(model, messages, provider='auto', temperature=0.7, max_tokens=512, **kwargs)`: Stream chat responses
- `list_models(provider=None)`: List available models
- `get_model_info(model)`: Get information about a model
- `conversation(model, system_prompt=None, ...)`: Create a conversation context

### Conversation Class

Class for managing multi-turn conversations.

#### Methods

- `send(message)`: Send a message and get response
- `stream_send(message)`: Send a message and stream response
- `reset()`: Reset conversation history
- `get_history()`: Get conversation history

## Advanced Usage

### Custom Message Format

```python
messages = [
    {"role": "system", "content": "You are a coding assistant."},
    {"role": "user", "content": "How do I sort a list?"},
    {"role": "assistant", "content": "You can use sorted() or .sort()"},
    {"role": "user", "content": "Show me an example"},
]

response = wrapper.chat(model="gpt-3.5-turbo", messages=messages)
```

### Provider Selection

```python
# Auto-detect provider from model name
response = wrapper.chat(model="gpt-3.5-turbo", messages="Hello")

# Explicitly specify provider
response = wrapper.chat(
    model="mistralai/Mistral-7B-Instruct-v0.2",
    messages="Hello",
    provider="huggingface",
)
```

### Local HuggingFace Models

```python
# Use local models (requires transformers and torch)
wrapper = ChatbotWrapper(
    use_local_hf=True,
    hf_device="cuda",  # or "cpu"
)

response = wrapper.chat(
    model="microsoft/DialoGPT-large",
    messages="Hello!",
)
```

## Configuration

You can customize the wrapper by modifying `config.py`:

- Add new models to `HUGGINGFACE_CHATBOT_MODELS` or `OPENAI_CHATBOT_MODELS`
- Adjust default parameters (temperature, max_tokens, etc.)
- Configure API endpoints

## Error Handling

The wrapper includes error handling for:

- Missing API keys
- Invalid model names
- API request failures
- Network errors

## Examples

See `examples.py` for comprehensive usage examples.

## Requirements

- Python 3.8+
- requests
- openai
- transformers (for local HuggingFace models)
- torch (for local HuggingFace models)

## License

This project is part of the capstone project template.


