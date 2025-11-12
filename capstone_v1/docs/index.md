---
layout: default
title: Home
nav_order: 1
---

# Chatbot API Wrapper Documentation

Welcome to the comprehensive documentation for the Chatbot API Wrapper. This project provides a unified interface for interacting with chatbot models from HuggingFace and OpenAI.

## Quick Start

Get up and running in minutes:

1. [Installation & Setup](getting-started.md#installation)
2. [Basic Usage](getting-started.md#basic-usage)
3. [Try the Chatbot Interface](chatbot-interface.html)

## Features

- **Unified Interface**: Single API for both HuggingFace and OpenAI models
- **Multiple Providers**: Support for cloud APIs and local models
- **Specialized Models**: Pre-configured with popular chatbot models
- **Streaming Support**: Real-time streaming responses
- **Conversation Management**: Built-in context for multi-turn chats
- **Interactive UI**: Beautiful chatbot interface with light/dark themes
- **Starter Prompts**: 30+ domain-specific system prompts for various use cases
- **Dataset Loaders**: Unified interface for loading datasets from HuggingFace, Seaborn, scikit-learn, OpenML, GitHub, and URLs
- **Fine-tuning Support**: Tools to convert datasets to chat format for model fine-tuning

## Documentation Sections

### [Startup Guide](STARTUP_GUIDE.md)
Complete step-by-step guide for new users to get up and running.

### [Getting Started](getting-started.md)
Installation instructions and basic usage examples.

### [API Reference](api-reference.md)
Comprehensive API documentation with all endpoints, parameters, and return values.

### [API Endpoints](api-endpoints.md)
Detailed reference for all API endpoints and methods.

### [Chatbot Interface](chatbot-interface.html)
Interactive web-based chatbot interface for testing models.

### [Examples](examples.md)
Code examples and use cases for common scenarios.

### [New Features](../api_wrapper/FEATURES.md)
Comprehensive guide to starter prompts and dataset loaders.

## Supported Models

### OpenAI Models
- GPT-4, GPT-4 Turbo
- GPT-3.5 Turbo variants

### HuggingFace Models
- Llama 2/3 (Meta)
- Mistral AI models
- DialoGPT (Microsoft)
- FLAN-T5 (Google)
- Zephyr (HuggingFace)

## Project Structure

```
capstone_v1/
├── api_wrapper/          # Main package
│   ├── __init__.py
│   ├── chatbot_wrapper.py
│   ├── huggingface_client.py
│   ├── openai_client.py
│   ├── config.py
│   ├── starter_prompts.py  # Domain-specific prompts
│   ├── dataset_loaders.py # Dataset loading utilities
│   └── examples.py        # Comprehensive examples
├── docs/                 # Documentation (this site)
└── requirements.txt      # Dependencies
```

## Need Help?

- Check the [Getting Started Guide](getting-started.md)
- Review [API Reference](api-reference.md)
- See [Examples](examples.md)
- Try the [Interactive Chatbot](chatbot-interface.html)

---

**Version**: 1.0.0  
**Last Updated**: 2024

