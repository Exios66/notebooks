---
layout: default
title: Examples
nav_order: 4
---

# Code Examples

Comprehensive examples for common use cases.

## Basic Examples

### Simple Chat

```python
from api_wrapper import ChatbotWrapper

# Initialize
wrapper = ChatbotWrapper(openai_api_key="your-key")

# Simple query
response = wrapper.chat(
    model="gpt-3.5-turbo",
    messages="What is machine learning?",
    temperature=0.7,
)

print(response['response'])
```

### Multi-turn Conversation

```python
from api_wrapper import ChatbotWrapper

wrapper = ChatbotWrapper(openai_api_key="your-key")

# Create conversation
conv = wrapper.conversation(
    model="gpt-3.5-turbo",
    system_prompt="You are a helpful coding assistant.",
)

# Multiple exchanges
print("User: How do I reverse a list?")
response1 = conv.send("How do I reverse a list in Python?")
print(f"Assistant: {response1}\n")

print("User: Show me an example")
response2 = conv.send("Can you show me an example?")
print(f"Assistant: {response2}")
```

### Streaming Response

```python
from api_wrapper import ChatbotWrapper

wrapper = ChatbotWrapper(openai_api_key="your-key")

print("Assistant: ", end="", flush=True)
for chunk in wrapper.stream_chat(
    model="gpt-3.5-turbo",
    messages="Tell me a short story about AI",
):
    print(chunk, end="", flush=True)
print()
```

## Advanced Examples

### Custom Message Format

```python
from api_wrapper import ChatbotWrapper

wrapper = ChatbotWrapper(openai_api_key="your-key")

messages = [
    {"role": "system", "content": "You are a Python expert."},
    {"role": "user", "content": "What is a list comprehension?"},
    {"role": "assistant", "content": "A list comprehension is a concise way to create lists."},
    {"role": "user", "content": "Show me an example"},
]

response = wrapper.chat(
    model="gpt-3.5-turbo",
    messages=messages,
    temperature=0.7,
)
print(response['response'])
```

### Provider Selection

```python
from api_wrapper import ChatbotWrapper, Provider

wrapper = ChatbotWrapper(
    openai_api_key="your-key",
    huggingface_api_key="your-key"
)

# Auto-detect
response1 = wrapper.chat(
    model="gpt-3.5-turbo",
    messages="Hello",
    provider=Provider.AUTO
)

# Explicit provider
response2 = wrapper.chat(
    model="mistralai/Mistral-7B-Instruct-v0.2",
    messages="Hello",
    provider=Provider.HUGGINGFACE
)
```

### Error Handling

```python
from api_wrapper import ChatbotWrapper

wrapper = ChatbotWrapper(openai_api_key="your-key")

try:
    response = wrapper.chat(
        model="gpt-3.5-turbo",
        messages="Hello",
        temperature=0.7,
    )
    print(response['response'])
except ValueError as e:
    print(f"Configuration error: {e}")
except Exception as e:
    print(f"API error: {e}")
```

## HuggingFace Examples

### Using Inference API

```python
from api_wrapper import ChatbotWrapper

wrapper = ChatbotWrapper(huggingface_api_key="your-key")

response = wrapper.chat(
    model="mistralai/Mistral-7B-Instruct-v0.2",
    messages="Explain quantum computing in simple terms.",
    provider="huggingface",
    temperature=0.7,
)

print(response['response'])
```

### Using Local Models

```python
from api_wrapper import ChatbotWrapper

# Initialize with local model support
wrapper = ChatbotWrapper(
    use_local_hf=True,
    hf_device="cuda"  # Use GPU if available
)

response = wrapper.chat(
    model="microsoft/DialoGPT-large",
    messages="Hello, how are you?",
    temperature=0.7,
)

print(response['response'])
```

## Model Management

### List Available Models

```python
from api_wrapper import ChatbotWrapper

wrapper = ChatbotWrapper(
    openai_api_key="your-key",
    huggingface_api_key="your-key"
)

# List all models
all_models = wrapper.list_models()
print("OpenAI models:", all_models["openai"])
print("HuggingFace models:", all_models["huggingface"])

# List specific provider
openai_models = wrapper.list_models(provider="openai")
print(openai_models)
```

### Get Model Information

```python
from api_wrapper import ChatbotWrapper

wrapper = ChatbotWrapper()

info = wrapper.get_model_info("gpt-3.5-turbo")
print(f"Name: {info['name']}")
print(f"Description: {info['description']}")
```

## Conversation Management

### Conversation with History

```python
from api_wrapper import ChatbotWrapper

wrapper = ChatbotWrapper(openai_api_key="your-key")

conv = wrapper.conversation(
    model="gpt-3.5-turbo",
    system_prompt="You are a helpful assistant.",
)

# Send messages
conv.send("What is Python?")
conv.send("What are its main features?")

# Get history
history = conv.get_history()
for msg in history:
    print(f"{msg['role']}: {msg['content']}")

# Reset conversation
conv.reset()
```

### Streaming Conversation

```python
from api_wrapper import ChatbotWrapper

wrapper = ChatbotWrapper(openai_api_key="your-key")

conv = wrapper.conversation(
    model="gpt-3.5-turbo",
    system_prompt="You are a storyteller.",
)

print("User: Tell me a story")
print("Assistant: ", end="", flush=True)

for chunk in conv.stream_send("Tell me a short story about space"):
    print(chunk, end="", flush=True)
print()
```

## Real-World Use Cases

### Code Assistant

```python
from api_wrapper import ChatbotWrapper

wrapper = ChatbotWrapper(openai_api_key="your-key")

conv = wrapper.conversation(
    model="gpt-3.5-turbo",
    system_prompt="You are an expert Python programmer. Provide clear, concise code examples.",
)

code_question = "How do I read a CSV file in Python?"
response = conv.send(code_question)
print(response)
```

### Content Generator

```python
from api_wrapper import ChatbotWrapper

wrapper = ChatbotWrapper(openai_api_key="your-key")

response = wrapper.chat(
    model="gpt-3.5-turbo",
    messages=[
        {"role": "system", "content": "You are a creative writer."},
        {"role": "user", "content": "Write a haiku about programming."},
    ],
    temperature=0.9,  # Higher temperature for creativity
)

print(response['response'])
```

### Data Analysis Assistant

```python
from api_wrapper import ChatbotWrapper

wrapper = ChatbotWrapper(openai_api_key="your-key")

conv = wrapper.conversation(
    model="gpt-3.5-turbo",
    system_prompt="You are a data science expert. Explain concepts clearly.",
)

questions = [
    "What is overfitting?",
    "How can I prevent it?",
    "What are some regularization techniques?",
]

for q in questions:
    print(f"\nUser: {q}")
    response = conv.send(q)
    print(f"Assistant: {response}")
```

## Performance Tips

### Batch Processing

```python
from api_wrapper import ChatbotWrapper

wrapper = ChatbotWrapper(openai_api_key="your-key")

questions = [
    "What is Python?",
    "What is machine learning?",
    "What is deep learning?",
]

responses = []
for q in questions:
    response = wrapper.chat(
        model="gpt-3.5-turbo",
        messages=q,
        temperature=0.7,
    )
    responses.append(response['response'])

for q, r in zip(questions, responses):
    print(f"Q: {q}\nA: {r}\n")
```

### Token Usage Tracking

```python
from api_wrapper import ChatbotWrapper

wrapper = ChatbotWrapper(openai_api_key="your-key")

response = wrapper.chat(
    model="gpt-3.5-turbo",
    messages="Explain neural networks",
)

if 'usage' in response:
    usage = response['usage']
    print(f"Prompt tokens: {usage['prompt_tokens']}")
    print(f"Completion tokens: {usage['completion_tokens']}")
    print(f"Total tokens: {usage['total_tokens']}")
```

## Integration Examples

### Flask Web App

```python
from flask import Flask, request, jsonify
from api_wrapper import ChatbotWrapper

app = Flask(__name__)
wrapper = ChatbotWrapper(openai_api_key="your-key")

@app.route('/chat', methods=['POST'])
def chat():
    data = request.json
    response = wrapper.chat(
        model=data.get('model', 'gpt-3.5-turbo'),
        messages=data['messages'],
        temperature=data.get('temperature', 0.7),
    )
    return jsonify(response)

if __name__ == '__main__':
    app.run(debug=True)
```

### Command Line Interface

```python
import sys
from api_wrapper import ChatbotWrapper

wrapper = ChatbotWrapper(openai_api_key="your-key")

if len(sys.argv) < 2:
    print("Usage: python cli.py 'your message'")
    sys.exit(1)

message = " ".join(sys.argv[1:])
response = wrapper.chat(
    model="gpt-3.5-turbo",
    messages=message,
)

print(response['response'])
```
