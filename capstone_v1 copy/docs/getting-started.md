---
layout: default
title: Getting Started
nav_order: 2
---

# Getting Started

This guide will help you set up and start using the Chatbot API Wrapper.

## Prerequisites

- Python 3.8 or higher
- pip (Python package manager)
- API keys (optional, depending on usage):
  - OpenAI API key (for OpenAI models)
  - HuggingFace API key (for HuggingFace Inference API)

## Installation

### Step 1: Clone or Navigate to the Repository

```bash
cd capstone_v1
```

### Step 2: Install Dependencies

Install all required packages:

```bash
pip install -r requirements.txt
```

This will install:

- `requests` - For HTTP requests
- `openai` - OpenAI Python SDK
- `transformers` - For local HuggingFace models
- `torch` - PyTorch for local model inference
- `accelerate` - For model acceleration

### Step 3: Set Up API Keys

You can set API keys in two ways:

#### Option A: Environment Variables (Recommended)

**Linux/macOS:**

```bash
export OPENAI_API_KEY="your-openai-api-key-here"
export HUGGINGFACE_API_KEY="your-huggingface-api-key-here"
```

**Windows (PowerShell):**

```powershell
$env:OPENAI_API_KEY="your-openai-api-key-here"
$env:HUGGINGFACE_API_KEY="your-huggingface-api-key-here"
```

**Windows (Command Prompt):**

```cmd
set OPENAI_API_KEY=your-openai-api-key-here
set HUGGINGFACE_API_KEY=your-huggingface-api-key-here
```

#### Option B: Pass Directly in Code

```python
from api_wrapper import ChatbotWrapper

wrapper = ChatbotWrapper(
    openai_api_key="your-key-here",
    huggingface_api_key="your-key-here"
)
```

### Step 4: Verify Installation

Test your installation:

```python
from api_wrapper import ChatbotWrapper

# Initialize wrapper
wrapper = ChatbotWrapper(openai_api_key="your-key")

# Test a simple query
response = wrapper.chat(
    model="gpt-3.5-turbo",
    messages="Hello, world!",
)
print(response['response'])
```

## Basic Usage

### Simple Chat

```python
from api_wrapper import ChatbotWrapper

# Initialize
wrapper = ChatbotWrapper(openai_api_key="your-key")

# Send a message
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

# Create conversation context
conv = wrapper.conversation(
    model="gpt-3.5-turbo",
    system_prompt="You are a helpful coding assistant.",
)

# Send messages
response1 = conv.send("How do I reverse a list in Python?")
print(response1)

response2 = conv.send("Can you show me an example?")
print(response2)
```

### Streaming Responses

```python
from api_wrapper import ChatbotWrapper

wrapper = ChatbotWrapper(openai_api_key="your-key")

# Stream response
for chunk in wrapper.stream_chat(
    model="gpt-3.5-turbo",
    messages="Tell me a story",
):
    print(chunk, end='', flush=True)
```

### Using HuggingFace Models

```python
from api_wrapper import ChatbotWrapper

# Via Inference API
wrapper = ChatbotWrapper(huggingface_api_key="your-key")

response = wrapper.chat(
    model="mistralai/Mistral-7B-Instruct-v0.2",
    messages="Explain quantum computing",
    provider="huggingface",
)
print(response['response'])
```

### Using Local Models

For local HuggingFace models (requires GPU recommended):

```python
from api_wrapper import ChatbotWrapper

# Use local models
wrapper = ChatbotWrapper(
    use_local_hf=True,
    hf_device="cuda"  # or "cpu" if no GPU
)

response = wrapper.chat(
    model="microsoft/DialoGPT-large",
    messages="Hello!",
)
print(response['response'])
```

## Configuration

### Default Parameters

You can customize default parameters in `api_wrapper/config.py`:

- `DEFAULT_TEMPERATURE`: 0.7
- `DEFAULT_MAX_TOKENS`: 512
- `DEFAULT_TOP_P`: 0.9
- `DEFAULT_TOP_K`: 50

### Adding New Models

Edit `api_wrapper/config.py` to add new models:

```python
HUGGINGFACE_CHATBOT_MODELS = {
    "your-model/name": {
        "name": "Model Display Name",
        "provider": "huggingface",
        "type": "inference",
        "description": "Model description",
    },
}
```

## Troubleshooting

### Common Issues

#### 1. Import Errors

- Ensure all dependencies are installed: `pip install -r requirements.txt`
- Check Python version: `python --version` (should be 3.8+)

#### 2. API Key Errors

- Verify API keys are set correctly
- Check environment variables: `echo $OPENAI_API_KEY`
- Ensure keys are valid and have proper permissions

#### 3. Model Loading Errors (Local)

- Ensure you have sufficient RAM/VRAM
- Check if model exists on HuggingFace
- Verify transformers and torch are installed correctly

#### 4. Network Errors

- Check internet connection
- Verify API endpoints are accessible
- Check firewall settings

#### Getting Help

- Review the [API Reference](api-reference.md)
- Check [Examples](examples.md)
- Review error messages for specific issues

## Next Steps

- **[🚀 Try the Interactive Chatbot Interface →](chatbot-interface.html)** - Experience the new HuggingChat-inspired UI with Omni mode
- Read the [API Reference](api-reference.md) for detailed documentation
- Explore [Code Examples](examples.md)

<div style="background: #f0f9ff; border-left: 4px solid #10a37f; padding: 1rem; margin: 1.5rem 0; border-radius: 4px;">
    <strong>💡 Pro Tip:</strong> The chatbot interface now features <strong>Omni mode</strong> which automatically selects the best model for your query. No need to manually choose between models!
</div>
