# Models Registry

This directory contains comprehensive information and endpoints for publicly sourceable models supported by the Chatbot API Wrapper.

## Overview

The models registry provides detailed information about each model including:

- **Full model identifiers** and names
- **API endpoints** with authentication requirements
- **Access methods** (API, local, or both)
- **Model specifications** (parameters, context windows, architecture)
- **Licensing information** and terms
- **Cost information** and free tier availability
- **Recommended use cases** and limitations
- **Documentation links** and model cards
- **Technical details** (supported languages, default parameters)

## Files

- **`models_registry.py`**: Python module containing the complete models registry with structured data classes
- **`models_registry.json`**: JSON export of all models for easy programmatic access
- **`README.md`**: This file

## Usage

### Python

```python
from models.models_registry import (
    get_model_info,
    list_models_by_provider,
    list_models_by_type,
    search_models,
    get_free_models,
    get_local_models,
    ALL_MODELS
)

# Get information about a specific model
model_info = get_model_info("meta-llama/Llama-2-7b-chat-hf")
print(f"Model: {model_info.name}")
print(f"Context Window: {model_info.specs.context_window}")
print(f"API Endpoint: {model_info.api_endpoint.url}")

# List all HuggingFace models
hf_models = list_models_by_provider("huggingface")

# List all chat models
chat_models = list_models_by_type(ModelType.CHAT)

# Search for models
results = search_models("instruction")

# Get free tier models
free_models = get_free_models()

# Get models that can run locally
local_models = get_local_models()
```

### JSON

```python
import json
from models.models_registry import export_to_dict

# Export to dictionary/JSON
models_dict = export_to_dict()
with open("models_registry.json", "w") as f:
    json.dump(models_dict, f, indent=2)
```

## Model Categories

### By Provider

#### HuggingFace Models

- **Llama Models**: Llama 2 (7B, 13B), Llama 3 (8B)
- **Mistral Models**: Mistral 7B Instruct, Mixtral 8x7B Instruct
- **Google Models**: FLAN-T5 XXL, Gemma 7B Instruct
- **Microsoft Models**: DialoGPT Large
- **HuggingFace Models**: Zephyr 7B Beta
- **Other**: Qwen 2.5 7B Instruct

#### OpenAI Models

- **GPT-4 Series**: GPT-4, GPT-4 Turbo, GPT-4 Turbo Preview, GPT-4o, GPT-4o Mini
- **GPT-3.5 Series**: GPT-3.5 Turbo, GPT-3.5 Turbo 16K

### By Type

- **Chat Models**: Optimized for conversational interactions
- **Instruct Models**: Instruction-following models
- **Multimodal Models**: Support for text and vision inputs
- **Completion Models**: Text completion tasks

## Access Methods

### API Access

Most models support API access through their respective providers:

- **HuggingFace**: Inference API at `https://api-inference.huggingface.co/models/{model_id}`
- **OpenAI**: Chat Completions API at `https://api.openai.com/v1/chat/completions`

### Local Access

Many HuggingFace models can be loaded and run locally using the `transformers` library:

```python
from transformers import AutoTokenizer, AutoModelForCausalLM

model_id = "meta-llama/Llama-2-7b-chat-hf"
tokenizer = AutoTokenizer.from_pretrained(model_id)
model = AutoModelForCausalLM.from_pretrained(model_id)
```

## API Keys

### HuggingFace

1. Create an account at [huggingface.co](https://huggingface.co)
2. Generate an API token at [huggingface.co/settings/tokens](https://huggingface.co/settings/tokens)
3. Set environment variable: `export HUGGINGFACE_API_KEY="your-token"`
4. For gated models (e.g., Llama), request access on the model page

### OpenAI

1. Create an account at [platform.openai.com](https://platform.openai.com)
2. Generate an API key at [platform.openai.com/api-keys](https://platform.openai.com/api-keys)
3. Set environment variable: `export OPENAI_API_KEY="your-key"`
4. Add billing information for API usage

## Free Tier Information

### HuggingFace Free Tier

- **Rate Limit**: 30 requests/minute (varies by model)
- **No credit card required**
- **Gated models**: Require account approval

### OpenAI Usage and Pricing

- **No free tier** (requires paid API access)
- **Pricing**: Pay-per-use based on tokens
- **Free credits**: May be available for new accounts

## Model Selection Guide

### For Conversational AI

- **Recommended**: `gpt-3.5-turbo`, `meta-llama/Llama-2-7b-chat-hf`, `microsoft/DialoGPT-large`
- **Best for**: Chatbots, customer support, general Q&A

### For Instruction Following

- **Recommended**: `mistralai/Mistral-7B-Instruct-v0.2`, `meta-llama/Meta-Llama-3-8B-Instruct`, `HuggingFaceH4/zephyr-7b-beta`
- **Best for**: Task completion, code generation, structured outputs

### For Complex Reasoning

- **Recommended**: `gpt-4`, `gpt-4-turbo`, `mistralai/Mixtral-8x7B-Instruct-v0.1`
- **Best for**: Advanced problem solving, analysis, synthesis

### For Cost-Effective Applications

- **Recommended**: `gpt-3.5-turbo`, `gpt-4o-mini`, `meta-llama/Llama-2-7b-chat-hf` (local)
- **Best for**: High-volume applications, prototyping

### For Long Context

- **Recommended**: `gpt-4-turbo`, `gpt-4o`, `mistralai/Mixtral-8x7B-Instruct-v0.1`, `Qwen/Qwen2.5-7B-Instruct`
- **Best for**: Document analysis, long conversations, code review

### For Local Deployment

- **Recommended**: `meta-llama/Llama-2-7b-chat-hf`, `mistralai/Mistral-7B-Instruct-v0.2`, `microsoft/DialoGPT-large`
- **Best for**: Privacy-sensitive applications, offline use, cost control

## Licensing

### Open Source Licenses

- **Apache 2.0**: Mistral, FLAN-T5, Gemma, Qwen, Zephyr
- **MIT**: DialoGPT, Zephyr
- **Llama 2 Community License**: Llama 2 models (requires Meta approval)
- **Llama 3 Community License**: Llama 3 models

### Proprietary

- **OpenAI Models**: Proprietary, requires API access

Always review the specific license terms before using a model in production.

## Model Specifications

### Parameter Counts

- **Small (< 1B)**: DialoGPT Large (774M)
- **Medium (1-10B)**: Llama 2 7B, Mistral 7B, Llama 3 8B, Gemma 7B, Qwen 2.5 7B
- **Large (10-50B)**: Llama 2 13B, FLAN-T5 XXL (11B), Mixtral 8x7B (47B effective)
- **Very Large (> 50B)**: GPT-4, GPT-4 Turbo (exact counts not disclosed)

### Context Windows

- **Small (512-1K)**: FLAN-T5 XXL (512), DialoGPT Large (1K)
- **Medium (4K-8K)**: Llama 2 (4K), Mistral 7B (8K), Gemma 7B (8K)
- **Large (16K-32K)**: GPT-3.5 Turbo (16K), Mixtral 8x7B (32K), Qwen 2.5 7B (32K)
- **Very Large (128K+)**: GPT-4 Turbo (128K), GPT-4o (128K)

## Integration with Chatbot Wrapper

The models registry is designed to work seamlessly with the Chatbot API Wrapper:

```python
from api_wrapper import ChatbotWrapper
from models.models_registry import get_model_info

# Get model information
model_info = get_model_info("gpt-3.5-turbo")

# Initialize wrapper
wrapper = ChatbotWrapper(openai_api_key="your-key")

# Use the model
response = wrapper.chat(
    model=model_info.model_id,
    messages="Hello!",
    temperature=model_info.default_temperature,
    max_tokens=model_info.default_max_tokens
)
```

## Adding New Models

To add a new model to the registry:

1. Create a new `ModelInfo` instance in `models_registry.py`
2. Add it to the appropriate dictionary (`HUGGINGFACE_MODELS` or `OPENAI_MODELS`)
3. Include all required fields:
   - Model ID, name, provider, type
   - API endpoint configuration
   - Model specifications
   - Licensing information
   - Use cases and limitations

Example:

```python
"new-model-id": ModelInfo(
    model_id="new-model-id",
    name="New Model Name",
    provider="huggingface",
    type=ModelType.CHAT,
    access_method=AccessMethod.BOTH,
    description="Model description",
    api_endpoint=ModelEndpoint(
        url="https://api-inference.huggingface.co/models/new-model-id",
        method="POST",
        auth_required=True,
    ),
    # ... other fields
)
```

## Resources

- [HuggingFace Model Hub](https://huggingface.co/models)
- [OpenAI Models Documentation](https://platform.openai.com/docs/models)
- [Transformers Library](https://huggingface.co/docs/transformers)
- [Model Cards](https://modelcards.withgoogle.com/)

## Support

For issues or questions about specific models:

- **HuggingFace**: Check model card and discussions on HuggingFace Hub
- **OpenAI**: See [OpenAI Documentation](https://platform.openai.com/docs) and [Support](https://help.openai.com)
