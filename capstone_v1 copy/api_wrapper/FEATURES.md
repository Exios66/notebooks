# New Features Documentation

## Overview

This document describes the comprehensive additions to the Chatbot API Wrapper, including:

- Expanded examples library
- Assistant starter prompts
- Dataset loaders for fine-tuning

## 1. Comprehensive Examples (`examples.py`)

The examples file has been expanded from 7 to 21+ examples covering:

### Basic Examples

- Basic usage
- Multi-turn conversations
- Streaming responses
- Message formatting
- Model listing

### Advanced Examples

- **Starter Prompts**: Using domain-specific system prompts
- **Domain-Specific**: Examples for different domains (data science, math, etc.)
- **Temperature Variations**: Comparing different temperature settings
- **Batch Processing**: Processing multiple queries
- **Error Handling**: Proper error handling patterns
- **Conversation History**: Managing conversation context
- **Provider Comparison**: Comparing OpenAI vs HuggingFace
- **Custom Parameters**: Using advanced parameters
- **Streaming Conversations**: Streaming in multi-turn chats
- **Model Information**: Getting model details
- **Advanced Message Formatting**: Complex conversation structures

### Dataset Examples

- **Dataset Loading**: Loading datasets from various sources
- **Dataset Conversion**: Converting datasets to chat format for fine-tuning

## 2. Starter Prompts (`starter_prompts.py`)

A comprehensive collection of system prompts for various domains:

### General Purpose

- `general`: General helpful assistant
- `friendly`: Friendly and approachable
- `professional`: Professional and formal

### Technical & Programming

- `coding`: Expert programming assistant
- `python`: Python programming expert
- `data_science`: Data science assistant
- `ml_engineer`: Machine learning engineer
- `devops`: DevOps assistant
- `security`: Cybersecurity expert
- `database`: Database administrator
- `frontend`: Frontend developer
- `backend`: Backend developer

### Educational

- `tutor`: Patient tutor
- `math`: Mathematics tutor
- `science`: Science tutor
- `language`: Language learning assistant

### Creative & Writing

- `creative_writer`: Creative writing assistant
- `content_writer`: Content writing assistant
- `technical_writer`: Technical writing assistant

### Business & Professional

- `business`: Business assistant
- `project_manager`: Project management assistant
- `resume`: Resume and career assistant

### Health & Wellness

- `health`: Health information assistant
- `fitness`: Fitness and nutrition assistant

### Research & Analysis

- `research`: Research assistant
- `data_analyst`: Data analyst assistant
- `academic`: Academic writing assistant
- `literature`: Literature review assistant

### Specialized

- `customer_service`: Customer service representative
- `translator`: Translation assistant
- `legal`: Legal information assistant
- `gaming`: Gaming assistant
- `ai_ethics`: AI ethics assistant

### Usage

```python
from api_wrapper.starter_prompts import get_prompt

# Get a prompt by name
coding_prompt = get_prompt("coding")

# Use in conversation
conv = wrapper.conversation(
    model="gpt-3.5-turbo",
    system_prompt=coding_prompt,
)
```

## 3. Dataset Loaders (`dataset_loaders.py`)

A unified interface for loading datasets from multiple sources for fine-tuning:

### Supported Sources

#### HuggingFace Datasets

- **Instruction Following**: Alpaca, Dolly, OpenOrca, UltraChat, ShareGPT
- **Question Answering**: SQuAD, Natural Questions, MS MARCO
- **Conversational**: PersonaChat, Wizard of Wikipedia, Empathetic Dialogues
- **Code**: The Stack, Code Search Net, GitHub Python
- **Summarization**: CNN/DailyMail, XSum, SamSum
- **Translation**: OPUS, WMT14, Flores
- **Sentiment**: IMDB, Yelp Reviews, Amazon Polarity
- **Classification**: AG News, DBPedia, Yahoo Answers
- **Math & Reasoning**: GSM8K, MATH, MMLU, HellaSwag, ARC
- **Safety**: Anthropic HH, OpenAssistant, BeaverTails

#### Seaborn Datasets

- anscombe, attention, brain_networks, car_crashes, diamonds, dots, exercise, flights, fmri, geyser, iris, mpg, penguins, planets, tips, titanic

#### Scikit-learn Datasets

- iris, wine, breast_cancer, diabetes

#### OpenML Datasets

- adult, bank_marketing, credit_g, diabetes, heart_disease, mushroom, nursery, tic_tac_toe, vote, zoo

#### GitHub & URLs

- Load datasets directly from GitHub repositories
- Load from any URL (CSV, JSON, TSV, Parquet)

### Usage Examples

```python
from api_wrapper.dataset_loaders import DatasetLoader

loader = DatasetLoader()

# Load from HuggingFace
dataset = loader.load_huggingface("alpaca", split="train")

# Load from Seaborn
df = loader.load_seaborn("titanic")

# Load from scikit-learn
data = loader.load_sklearn("iris")

# Load from OpenML
df = loader.load_openml("adult")

# Load from GitHub
df = loader.load_from_github(
    "https://github.com/user/repo",
    "data.csv"
)

# Load from URL
df = loader.load_from_url("https://example.com/data.csv")

# Convert to chat format for fine-tuning
chat_data = loader.convert_to_chat_format(
    dataset,
    instruction_col="instruction",
    input_col="input",
    output_col="output"
)

# Save in various formats
loader.save_chat_format(chat_data, "output.jsonl", format="jsonl")
```

## Installation

Install all dependencies:

```bash
pip install -r requirements.txt
```

Key new dependencies:

- `datasets>=2.14.0` - HuggingFace datasets
- `huggingface-hub>=0.16.0` - HuggingFace Hub access
- `pandas>=2.0.0` - Data manipulation
- `seaborn>=0.12.0` - Seaborn datasets
- `openpyxl>=3.1.0` - Excel support
- `pyarrow>=12.0.0` - Parquet support

## Quick Start

### Using Starter Prompts

```python
from api_wrapper import ChatbotWrapper, get_prompt

wrapper = ChatbotWrapper(openai_api_key="your-key")

# Create a domain-specific assistant
conv = wrapper.conversation(
    model="gpt-3.5-turbo",
    system_prompt=get_prompt("data_science"),
)

response = conv.send("Explain overfitting in machine learning")
```

### Loading Datasets

```python
from api_wrapper import DatasetLoader

loader = DatasetLoader()

# Load a dataset
dataset = loader.load_huggingface("alpaca", split="train")

# Convert to chat format
chat_data = loader.convert_to_chat_format(
    dataset,
    instruction_col="instruction",
    output_col="output"
)
```

### Running Examples

```python
# Run all examples
python -m api_wrapper.examples

# Or import specific examples
from api_wrapper.examples import example_starter_prompts
example_starter_prompts()
```

## Best Practices

1. **Starter Prompts**: Use domain-specific prompts for better results
2. **Dataset Selection**: Choose datasets appropriate for your fine-tuning task
3. **Chat Format**: Always convert datasets to chat format before fine-tuning
4. **Error Handling**: Wrap dataset loading in try-except blocks
5. **Caching**: Datasets are cached automatically to avoid re-downloading

## Additional Resources

- See `examples.py` for comprehensive usage examples
- See `starter_prompts.py` for all available prompts
- See `dataset_loaders.py` for dataset loading documentation
