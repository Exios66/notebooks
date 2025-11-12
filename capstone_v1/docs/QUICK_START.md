# Quick Start Guide

Get up and running in 5 minutes!

## 1. Install Dependencies

```bash
cd capstone_v1
pip install -r requirements.txt
```

## 2. Set API Key

**macOS/Linux:**

```bash
export OPENAI_API_KEY="sk-your-key-here"
```

**Windows:**

```cmd
set OPENAI_API_KEY=sk-your-key-here
```

## 3. Test It

```python
from api_wrapper import ChatbotWrapper

wrapper = ChatbotWrapper(openai_api_key="your-key")

response = wrapper.chat(
    model="gpt-3.5-turbo",
    messages="Hello!",
)

print(response['response'])
```

## 4. Try the Web Interface

Open `docs/chatbot-interface.html` in your browser!

## That's It

- Need more help? See [STARTUP_GUIDE.md](STARTUP_GUIDE.md)
- Want examples? See [examples.md](examples.md)
- Need API docs? See [api-reference.md](api-reference.md)
