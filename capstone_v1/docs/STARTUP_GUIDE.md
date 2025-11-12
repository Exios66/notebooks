# Complete Startup Guide

This guide will walk you through everything needed to get the Chatbot API Wrapper up and running from scratch.

## Table of Contents

1. [Prerequisites](#prerequisites)
2. [Installation](#installation)
3. [Configuration](#configuration)
4. [Verification](#verification)
5. [First Steps](#first-steps)
6. [Troubleshooting](#troubleshooting)

## Prerequisites

### System Requirements

- **Operating System**: Windows, macOS, or Linux
- **Python**: Version 3.8 or higher
- **Internet Connection**: Required for API calls and package installation
- **API Keys**: OpenAI and/or HuggingFace API keys (depending on usage)

### Check Python Installation

```bash
python --version
# Should show Python 3.8 or higher

# Or try:
python3 --version
```

If Python is not installed, download from [python.org](https://www.python.org/downloads/).

### Check pip Installation

```bash
pip --version
# Or:
pip3 --version
```

If pip is not installed, install it with:

```bash
python -m ensurepip --upgrade
```

## Installation

### Step 1: Navigate to Project Directory

```bash
cd capstone_v1
```

### Step 2: Create Virtual Environment (Recommended)

**Windows:**

```cmd
python -m venv venv
venv\Scripts\activate
```

**macOS/Linux:**

```bash
python3 -m venv venv
source venv/bin/activate
```

### Step 3: Install Dependencies

```bash
pip install -r requirements.txt
```

This installs:

- `requests` - HTTP library
- `openai` - OpenAI Python SDK
- `transformers` - HuggingFace transformers
- `torch` - PyTorch for local models
- `accelerate` - Model acceleration

**Note**: Installation may take several minutes, especially for PyTorch.

### Step 4: Verify Installation

```python
python -c "from api_wrapper import ChatbotWrapper; print('Installation successful!')"
```

If no errors appear, installation is complete.

## Configuration

### Option 1: Environment Variables (Recommended)

#### Windows (Command Prompt)

```cmd
set OPENAI_API_KEY=sk-your-key-here
set HUGGINGFACE_API_KEY=hf_your-key-here
```

#### Windows (PowerShell)

```powershell
$env:OPENAI_API_KEY="sk-your-key-here"
$env:HUGGINGFACE_API_KEY="hf_your-key-here"
```

#### macOS/Linux

```bash
export OPENAI_API_KEY="sk-your-key-here"
export HUGGINGFACE_API_KEY="hf_your-key-here"
```

**Persistent Setup (macOS/Linux):**

Add to `~/.bashrc` or `~/.zshrc`:

```bash
export OPENAI_API_KEY="sk-your-key-here"
export HUGGINGFACE_API_KEY="hf_your-key-here"
```

Then reload:

```bash
source ~/.bashrc  # or source ~/.zshrc
```

### Option 2: Direct in Code

```python
from api_wrapper import ChatbotWrapper

wrapper = ChatbotWrapper(
    openai_api_key="sk-your-key-here",
    huggingface_api_key="hf_your-key-here"
)
```

### Getting API Keys

#### OpenAI API Key

1. Go to [platform.openai.com](https://platform.openai.com)
2. Sign up or log in
3. Navigate to API Keys section
4. Create a new secret key
5. Copy and save the key (starts with `sk-`)

#### HuggingFace API Key

1. Go to [huggingface.co](https://huggingface.co)
2. Sign up or log in
3. Go to Settings → Access Tokens
4. Create a new token
5. Copy and save the token (starts with `hf_`)

## Verification

### Test Script

Create a file `test_setup.py`:

```python
from api_wrapper import ChatbotWrapper
import os

# Check API keys
openai_key = os.getenv("OPENAI_API_KEY")
hf_key = os.getenv("HUGGINGFACE_API_KEY")

print("API Keys Status:")
print(f"OpenAI: {'✓ Set' if openai_key else '✗ Not set'}")
print(f"HuggingFace: {'✓ Set' if hf_key else '✗ Not set'}")

# Test wrapper initialization
try:
    wrapper = ChatbotWrapper(
        openai_api_key=openai_key,
        huggingface_api_key=hf_key
    )
    print("\n✓ Wrapper initialized successfully!")
    
    # Test model listing
    models = wrapper.list_models()
    print(f"\nAvailable models:")
    print(f"OpenAI: {len(models.get('openai', []))} models")
    print(f"HuggingFace: {len(models.get('huggingface', []))} models")
    
except Exception as e:
    print(f"\n✗ Error: {e}")
```

Run it:

```bash
python test_setup.py
```

### Quick Test

```python
from api_wrapper import ChatbotWrapper

wrapper = ChatbotWrapper(openai_api_key="your-key")

response = wrapper.chat(
    model="gpt-3.5-turbo",
    messages="Say 'Hello, World!'",
)

print(response['response'])
```

Expected output: "Hello, World!" or similar greeting.

## First Steps

### 1. Basic Chat

```python
from api_wrapper import ChatbotWrapper

wrapper = ChatbotWrapper(openai_api_key="your-key")

response = wrapper.chat(
    model="gpt-3.5-turbo",
    messages="What is Python?",
    temperature=0.7,
)

print(response['response'])
```

### 2. Multi-turn Conversation

```python
from api_wrapper import ChatbotWrapper

wrapper = ChatbotWrapper(openai_api_key="your-key")

conv = wrapper.conversation(
    model="gpt-3.5-turbo",
    system_prompt="You are a helpful assistant.",
)

response1 = conv.send("What is machine learning?")
print(response1)

response2 = conv.send("Give me an example.")
print(response2)
```

### 3. Try the Web Interface

1. Open `docs/chatbot-interface.html` in a web browser (or visit it on GitHub Pages)
2. Click "Settings" and enter your API key
3. Try **Omni mode** (automatically selects the best model) or choose a specific model
4. Start chatting!

**✨ New Features:**

- **Omni Mode**: Automatically picks the best AI model for your query
- **Model Selection**: Choose from OpenAI and HuggingFace models
- **Modern UI**: Clean, responsive design with dark mode support

### 4. Run Examples

```bash
cd api_wrapper
python examples.py
```

## Troubleshooting

### Common Issues

#### 1. Import Errors

**Error:** `ModuleNotFoundError: No module named 'api_wrapper'`

**Solution:**

```bash
# Make sure you're in the capstone_v1 directory
cd capstone_v1

# Verify the api_wrapper directory exists
ls api_wrapper

# Reinstall if needed
pip install -r requirements.txt
```

#### 2. API Key Errors

**Error:** `ValueError: OpenAI API key is required`

**Solution:**

- Verify API key is set: `echo $OPENAI_API_KEY` (Linux/macOS) or `echo %OPENAI_API_KEY%` (Windows)
- Check key format (OpenAI starts with `sk-`, HuggingFace starts with `hf_`)
- Ensure key is valid and has proper permissions

#### 3. Network Errors

**Error:** `ConnectionError` or `TimeoutError`

**Solution:**

- Check internet connection
- Verify firewall settings
- Try again (may be temporary API issue)
- Check API status pages

#### 4. Model Loading Errors (Local)

**Error:** `CUDA out of memory` or model loading fails

**Solution:**

- Use CPU instead: `hf_device="cpu"`
- Use smaller models
- Use Inference API instead: `use_local_hf=False`
- Ensure sufficient RAM/VRAM

#### 5. Package Installation Errors

**Error:** `ERROR: Could not build wheels`

**Solution:**

```bash
# Update pip
pip install --upgrade pip

# Install build tools (if needed)
# Windows: Install Visual C++ Build Tools
# macOS: xcode-select --install
# Linux: sudo apt-get install build-essential

# Try again
pip install -r requirements.txt
```

### Getting Help

1. Check the [API Reference](api-reference.md)
2. Review [Examples](examples.md)
3. Check error messages for specific issues
4. Verify API keys and permissions
5. Check API provider status pages

## Next Steps

- **[🚀 Try the Interactive Chatbot Interface →](chatbot-interface.html)** - Experience the new HuggingChat-inspired UI with Omni mode
- Read the [Getting Started Guide](getting-started.md)
- Explore the [API Reference](api-reference.md)
- Try [Code Examples](examples.md)

## Additional Resources

- [OpenAI Documentation](https://platform.openai.com/docs)
- [HuggingFace Documentation](https://huggingface.co/docs)
- [Python Documentation](https://docs.python.org/3/)

---

**Need more help?** Review the full documentation or check the troubleshooting section above.
