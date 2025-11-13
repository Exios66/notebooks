"""
Comprehensive Examples for the Chatbot API Wrapper
Covers various use cases, domains, and integration patterns
"""

import os
import sys
from pathlib import Path
import json

try:
    import pandas as pd
    PANDAS_AVAILABLE = True
except ImportError:
    PANDAS_AVAILABLE = False
    print("Note: pandas not available for dataset examples")

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))  # noqa: E402

from api_wrapper import ChatbotWrapper  # noqa: E402
try:
    from api_wrapper.starter_prompts import get_prompt, list_available_prompts
    PROMPTS_AVAILABLE = True
except ImportError:
    PROMPTS_AVAILABLE = False
    print("Note: starter_prompts module not available")

try:
    from api_wrapper.dataset_loaders import DatasetLoader, get_available_datasets
    DATASETS_AVAILABLE = True
except ImportError:
    DATASETS_AVAILABLE = False
    print("Note: dataset_loaders module not available")

try:
    from models.models_registry import (
        get_model_info,
        list_models_by_provider,
        list_models_by_type,
        search_models,
        get_free_models,
        get_local_models,
        ModelType,
        ALL_MODELS,
    )
    MODELS_REGISTRY_AVAILABLE = True
except ImportError:
    MODELS_REGISTRY_AVAILABLE = False
    print("Note: models registry not available")


def example_basic_usage():
    """Basic usage example"""
    print("=" * 50)
    print("Example 1: Basic Usage")
    print("=" * 50)

    # Initialize wrapper with API keys
    wrapper = ChatbotWrapper(
        openai_api_key=os.getenv("OPENAI_API_KEY"),
        huggingface_api_key=os.getenv("HUGGINGFACE_API_KEY"),
    )

    # Simple chat with OpenAI
    response = wrapper.chat(
        model="gpt-3.5-turbo",
        messages="What is machine learning?",
        temperature=0.7,
    )
    print(f"Response: {response['response']}\n")


def example_multi_turn_conversation():
    """Multi-turn conversation example"""
    print("=" * 50)
    print("Example 2: Multi-turn Conversation")
    print("=" * 50)

    wrapper = ChatbotWrapper(openai_api_key=os.getenv("OPENAI_API_KEY"))

    # Create a conversation context
    conv = wrapper.conversation(
        model="gpt-3.5-turbo",
        system_prompt="You are a helpful coding assistant.",
    )

    # Send multiple messages
    print("User: How do I reverse a list in Python?")
    response1 = conv.send("How do I reverse a list in Python?")
    print(f"Assistant: {response1}\n")

    print("User: Can you show me an example?")
    response2 = conv.send("Can you show me an example?")
    print(f"Assistant: {response2}\n")


def example_streaming():
    """Streaming response example"""
    print("=" * 50)
    print("Example 3: Streaming Responses")
    print("=" * 50)

    wrapper = ChatbotWrapper(openai_api_key=os.getenv("OPENAI_API_KEY"))

    print("User: Tell me a short story about AI")
    print("Assistant: ", end="", flush=True)

    for chunk in wrapper.stream_chat(
        model="gpt-3.5-turbo",
        messages="Tell me a short story about AI",
    ):
        print(chunk, end="", flush=True)
    print("\n")


def example_huggingface():
    """HuggingFace model example"""
    print("=" * 50)
    print("Example 4: HuggingFace Models")
    print("=" * 50)

    wrapper = ChatbotWrapper(
        huggingface_api_key=os.getenv("HUGGINGFACE_API_KEY"),
    )

    # Use a HuggingFace model
    response = wrapper.chat(
        model="mistralai/Mistral-7B-Instruct-v0.2",
        messages="Explain quantum computing in simple terms.",
        temperature=0.7,
    )
    print(f"Response: {response['response']}\n")


def example_local_huggingface():
    """Local HuggingFace model example"""
    print("=" * 50)
    print("Example 5: Local HuggingFace Models")
    print("=" * 50)

    # Use local models (requires GPU for best performance)
    wrapper = ChatbotWrapper(use_local_hf=True, hf_device="cuda")

    response = wrapper.chat(
        model="microsoft/DialoGPT-large",
        messages="Hello, how are you?",
        temperature=0.7,
    )
    print(f"Response: {response['response']}\n")


def example_list_models():
    """List available models"""
    print("=" * 50)
    print("Example 6: List Available Models")
    print("=" * 50)

    wrapper = ChatbotWrapper(
        openai_api_key=os.getenv("OPENAI_API_KEY"),
        huggingface_api_key=os.getenv("HUGGINGFACE_API_KEY"),
    )

    models = wrapper.list_models()
    print("Available models:")
    for provider, model_list in models.items():
        print(f"\n{provider.upper()}:")
        for model in model_list[:5]:  # Show first 5
            info = wrapper.get_model_info(model)
            print(f"  - {model}: {info.get('description', 'N/A')}")


def example_message_format():
    """Example with proper message formatting"""
    print("=" * 50)
    print("Example 7: Message Format")
    print("=" * 50)

    wrapper = ChatbotWrapper(openai_api_key=os.getenv("OPENAI_API_KEY"))

    # Use proper message format
    messages = [
        {"role": "system", "content": "You are a helpful assistant."},
        {"role": "user", "content": "What is Python?"},
        {"role": "assistant", "content": "Python is a programming language."},
        {"role": "user", "content": "What are its main features?"},
    ]

    response = wrapper.chat(
        model="gpt-3.5-turbo",
        messages=messages,
        temperature=0.7,
    )
    print(f"Response: {response['response']}\n")


def example_starter_prompts():
    """Example using starter prompts for different domains"""
    print("=" * 50)
    print("Example 8: Using Starter Prompts")
    print("=" * 50)

    if not PROMPTS_AVAILABLE:
        print("Starter prompts module not available. Skipping example.\n")
        return

    wrapper = ChatbotWrapper(openai_api_key=os.getenv("OPENAI_API_KEY"))

    # Use coding assistant prompt
    coding_prompt = get_prompt("coding")
    conv = wrapper.conversation(
        model="gpt-3.5-turbo",
        system_prompt=coding_prompt,
    )

    print("User: How do I implement a binary search in Python?")
    response = conv.send("How do I implement a binary search in Python?")
    print(f"Assistant: {response[:200]}...\n")  # Show first 200 chars


def example_domain_specific():
    """Examples for different domains"""
    print("=" * 50)
    print("Example 9: Domain-Specific Conversations")
    print("=" * 50)

    if not PROMPTS_AVAILABLE:
        print("Starter prompts module not available. Skipping example.\n")
        return

    wrapper = ChatbotWrapper(openai_api_key=os.getenv("OPENAI_API_KEY"))

    # Data Science Assistant
    print("\n--- Data Science Assistant ---")
    ds_conv = wrapper.conversation(
        model="gpt-3.5-turbo",
        system_prompt=get_prompt("data_science"),
    )
    response = ds_conv.send("What's the difference between L1 and L2 regularization?")
    print("Q: What's the difference between L1 and L2 regularization?")
    print(f"A: {response[:150]}...\n")

    # Math Tutor
    print("\n--- Math Tutor ---")
    math_conv = wrapper.conversation(
        model="gpt-3.5-turbo",
        system_prompt=get_prompt("math"),
    )
    response = math_conv.send("Explain the chain rule in calculus")
    print("Q: Explain the chain rule in calculus")
    print(f"A: {response[:150]}...\n")


def example_temperature_variations():
    """Example showing different temperature settings"""
    print("=" * 50)
    print("Example 10: Temperature Variations")
    print("=" * 50)

    wrapper = ChatbotWrapper(openai_api_key=os.getenv("OPENAI_API_KEY"))

    prompt = "Write a creative story about a robot learning to paint."

    print("\n--- Low Temperature (0.2) - More Deterministic ---")
    response_low = wrapper.chat(
        model="gpt-3.5-turbo",
        messages=prompt,
        temperature=0.2,
    )
    print(f"{response_low['response'][:200]}...\n")

    print("\n--- High Temperature (1.2) - More Creative ---")
    response_high = wrapper.chat(
        model="gpt-3.5-turbo",
        messages=prompt,
        temperature=1.2,
    )
    print(f"{response_high['response'][:200]}...\n")


def example_batch_processing():
    """Example of processing multiple queries"""
    print("=" * 50)
    print("Example 11: Batch Processing")
    print("=" * 50)

    wrapper = ChatbotWrapper(openai_api_key=os.getenv("OPENAI_API_KEY"))

    questions = [
        "What is machine learning?",
        "What is deep learning?",
        "What is reinforcement learning?",
    ]

    print("Processing multiple questions:\n")
    for i, question in enumerate(questions, 1):
        response = wrapper.chat(
            model="gpt-3.5-turbo",
            messages=question,
            temperature=0.7,
        )
        print(f"{i}. Q: {question}")
        print(f"   A: {response['response'][:100]}...\n")


def example_error_handling():
    """Example of error handling"""
    print("=" * 50)
    print("Example 12: Error Handling")
    print("=" * 50)

    wrapper = ChatbotWrapper(openai_api_key=os.getenv("OPENAI_API_KEY"))

    # Try with invalid model
    try:
        wrapper.chat(
            model="invalid-model-name",
            messages="Hello",
        )
    except Exception as e:
        print(f"Caught error: {type(e).__name__}: {e}\n")

    # Try with missing API key
    try:
        bad_wrapper = ChatbotWrapper(openai_api_key=None)
        bad_wrapper.chat(
            model="gpt-3.5-turbo",
            messages="Hello",
        )
    except Exception as e:
        print(f"Caught error: {type(e).__name__}: {e}\n")


def example_conversation_history():
    """Example showing conversation history management"""
    print("=" * 50)
    print("Example 13: Conversation History")
    print("=" * 50)

    wrapper = ChatbotWrapper(openai_api_key=os.getenv("OPENAI_API_KEY"))

    conv = wrapper.conversation(
        model="gpt-3.5-turbo",
        system_prompt="You are a helpful assistant.",
    )

    conv.send("My name is Alice.")
    conv.send("What's my name?")
    response = conv.send("What did I tell you my name was?")

    print(f"Final response: {response}\n")
    print("Conversation history:")
    history = conv.get_history()
    for i, msg in enumerate(history, 1):
        print(f"{i}. {msg['role']}: {msg['content'][:50]}...")

    # Reset conversation
    conv.reset()
    print(f"\nAfter reset, history length: {len(conv.get_history())}\n")


def example_provider_comparison():
    """Example comparing different providers"""
    print("=" * 50)
    print("Example 14: Provider Comparison")
    print("=" * 50)

    wrapper = ChatbotWrapper(
        openai_api_key=os.getenv("OPENAI_API_KEY"),
        huggingface_api_key=os.getenv("HUGGINGFACE_API_KEY"),
    )

    prompt = "Explain what Python is in one sentence."

    # OpenAI
    print("\n--- OpenAI (gpt-3.5-turbo) ---")
    try:
        response_openai = wrapper.chat(
            model="gpt-3.5-turbo",
            messages=prompt,
            provider="openai",
        )
        print(f"Response: {response_openai['response']}\n")
    except Exception as e:
        print(f"Error: {e}\n")

    # HuggingFace (if available)
    print("\n--- HuggingFace (Mistral) ---")
    try:
        response_hf = wrapper.chat(
            model="mistralai/Mistral-7B-Instruct-v0.2",
            messages=prompt,
            provider="huggingface",
        )
        print(f"Response: {response_hf['response']}\n")
    except Exception as e:
        print(f"Error: {e}\n")


def example_custom_parameters():
    """Example with custom parameters"""
    print("=" * 50)
    print("Example 15: Custom Parameters")
    print("=" * 50)

    wrapper = ChatbotWrapper(openai_api_key=os.getenv("OPENAI_API_KEY"))

    # Custom max_tokens
    response = wrapper.chat(
        model="gpt-3.5-turbo",
        messages="Write a haiku about programming.",
        temperature=0.8,
        max_tokens=100,  # Limit response length
    )
    print(f"Response (max_tokens=100): {response['response']}\n")

    # With frequency_penalty (OpenAI specific)
    response = wrapper.chat(
        model="gpt-3.5-turbo",
        messages="List 5 programming languages.",
        temperature=0.7,
        frequency_penalty=0.5,  # Reduce repetition
    )
    print(f"Response (with frequency_penalty): {response['response']}\n")


def example_dataset_loading():
    """Example of loading datasets for fine-tuning"""
    print("=" * 50)
    print("Example 16: Loading Datasets")
    print("=" * 50)

    if not DATASETS_AVAILABLE:
        print("Dataset loaders module not available. Skipping example.\n")
        return

    loader = DatasetLoader()

    # List available datasets
    print("\n--- Available Datasets ---")
    available = get_available_datasets()
    for source, datasets in available.items():
        print(f"\n{source.upper()}:")
        for ds in datasets[:5]:  # Show first 5
            print(f"  - {ds}")

    # Load Seaborn dataset
    print("\n--- Loading Seaborn Dataset ---")
    try:
        df = loader.load_seaborn("titanic")
        print(f"Loaded Titanic dataset: {df.shape[0]} rows, {df.shape[1]} columns")
        print(f"Columns: {', '.join(df.columns[:5])}...\n")
    except Exception as e:
        print(f"Error loading seaborn dataset: {e}\n")

    # Load scikit-learn dataset
    print("\n--- Loading Scikit-learn Dataset ---")
    try:
        data = loader.load_sklearn("iris")
        print("Loaded Iris dataset")
        if hasattr(data, 'data'):
            print(f"Features shape: {data.data.shape}")
            print(f"Target shape: {data.target.shape}\n")
    except Exception as e:
        print(f"Error loading sklearn dataset: {e}\n")


def example_dataset_conversion():
    """Example of converting datasets to chat format"""
    print("=" * 50)
    print("Example 17: Converting Datasets to Chat Format")
    print("=" * 50)

    if not DATASETS_AVAILABLE:
        print("Dataset loaders module not available. Skipping example.\n")
        return

    loader = DatasetLoader()

    # Create sample dataset
    print("\n--- Creating Sample Dataset ---")
    if not PANDAS_AVAILABLE:
        print("pandas not available. Skipping dataset conversion example.\n")
        return

    sample_data = pd.DataFrame({
        "instruction": [
            "What is Python?",
            "How do I sort a list?",
            "What is machine learning?",
        ],
        "input": ["", "", ""],
        "output": [
            "Python is a high-level programming language.",
            "You can use sorted() or .sort() method.",
            "Machine learning is a subset of AI.",
        ],
    })

    # Convert to chat format
    chat_data = loader.convert_to_chat_format(
        sample_data,
        instruction_col="instruction",
        input_col="input",
        output_col="output",
    )

    print(f"Converted {len(chat_data)} examples to chat format")
    print("\nFirst example:")
    print(json.dumps(chat_data[0], indent=2))

    # Save to file
    output_path = "/tmp/sample_chat_data.jsonl"
    loader.save_chat_format(chat_data, output_path, format="jsonl")
    print(f"\nSaved to {output_path}\n")


def example_streaming_conversation():
    """Example of streaming in a conversation"""
    print("=" * 50)
    print("Example 18: Streaming Conversation")
    print("=" * 50)

    wrapper = ChatbotWrapper(openai_api_key=os.getenv("OPENAI_API_KEY"))

    conv = wrapper.conversation(
        model="gpt-3.5-turbo",
        system_prompt="You are a helpful assistant.",
    )

    print("User: Tell me a short story about AI")
    print("Assistant: ", end="", flush=True)

    full_response = ""
    for chunk in conv.stream_send("Tell me a short story about AI"):
        print(chunk, end="", flush=True)
        full_response += chunk
    print("\n")


def example_model_info():
    """Example of getting model information"""
    print("=" * 50)
    print("Example 19: Model Information")
    print("=" * 50)

    wrapper = ChatbotWrapper(
        openai_api_key=os.getenv("OPENAI_API_KEY"),
        huggingface_api_key=os.getenv("HUGGINGFACE_API_KEY"),
    )

    models_to_check = [
        "gpt-3.5-turbo",
        "gpt-4",
        "mistralai/Mistral-7B-Instruct-v0.2",
    ]

    for model in models_to_check:
        info = wrapper.get_model_info(model)
        print(f"\n{model}:")
        print(f"  Description: {info.get('description', 'N/A')}")
        print(f"  Provider: {info.get('provider', 'N/A')}")


def example_advanced_message_formatting():
    """Example of advanced message formatting"""
    print("=" * 50)
    print("Example 20: Advanced Message Formatting")
    print("=" * 50)

    wrapper = ChatbotWrapper(openai_api_key=os.getenv("OPENAI_API_KEY"))

    # Complex conversation with context
    messages = [
        {
            "role": "system",
            "content": "You are a helpful coding assistant. You provide clear, well-documented code examples."
        },
        {
            "role": "user",
            "content": "I need to parse a CSV file in Python."
        },
        {
            "role": "assistant",
            "content": "You can use the pandas library. Here's an example:\n```python\nimport pandas as pd\ndf = pd.read_csv('file.csv')\n```"
        },
        {
            "role": "user",
            "content": "What if I want to handle missing values?"
        },
    ]

    response = wrapper.chat(
        model="gpt-3.5-turbo",
        messages=messages,
        temperature=0.7,
    )
    print(f"Response: {response['response']}\n")


def example_all_starter_prompts():
    """List all available starter prompts"""
    print("=" * 50)
    print("Example 21: Available Starter Prompts")
    print("=" * 50)

    if not PROMPTS_AVAILABLE:
        print("Starter prompts module not available.\n")
        return

    prompts = list_available_prompts()
    print(f"\nAvailable prompts ({len(prompts)} total):\n")
    for i, prompt_name in enumerate(prompts, 1):
        print(f"{i:2d}. {prompt_name}")


if __name__ == "__main__":
    # Set your API keys as environment variables
    # export OPENAI_API_KEY="your-key-here"
    # export HUGGINGFACE_API_KEY="your-key-here"

    # Basic examples (always run)
    basic_examples = [
        example_basic_usage,
        example_multi_turn_conversation,
        example_streaming,
        example_list_models,
        example_message_format,
        example_temperature_variations,
        example_error_handling,
        example_conversation_history,
        example_custom_parameters,
        example_streaming_conversation,
        example_model_info,
        example_advanced_message_formatting,
        example_all_starter_prompts,
        example_models_registry_info,
        example_models_registry_search,
        example_models_registry_free_tier,
        example_models_registry_local,
        example_models_registry_comparison,
    ]

    # Optional examples (require additional setup)
    optional_examples = [
        example_huggingface,  # Requires HF API key
        example_local_huggingface,  # Requires local models
        example_starter_prompts,  # Requires starter_prompts module
        example_domain_specific,  # Requires starter_prompts module
        example_batch_processing,
        example_provider_comparison,  # Requires both API keys
        example_dataset_loading,  # Requires dataset_loaders module
        example_dataset_conversion,  # Requires dataset_loaders module
        example_models_registry_integration,  # Requires models registry and API keys
    ]

    print("\n" + "=" * 70)
    print("CHATBOT API WRAPPER - COMPREHENSIVE EXAMPLES")
    print("=" * 70 + "\n")

    try:
        # Run basic examples
        for example_func in basic_examples:
            try:
                example_func()
            except Exception as e:
                print(f"Error in {example_func.__name__}: {e}\n")
                continue

        # Run optional examples (commented out by default)
        print("\n" + "=" * 70)
        print("OPTIONAL EXAMPLES (uncomment to run)")
        print("=" * 70 + "\n")
        print("To run optional examples, uncomment them in the code.\n")

        # Uncomment these to run:
        # for example_func in optional_examples:
        #     try:
        #         example_func()
        #     except Exception as e:
        #         print(f"Error in {example_func.__name__}: {e}\n")
        #         continue

    except KeyboardInterrupt:
        print("\n\nExamples interrupted by user.")
    except Exception as e:
        print(f"\nUnexpected error: {e}")
        print("\nMake sure to set your API keys as environment variables:")
        print("export OPENAI_API_KEY='your-key-here'")
        print("export HUGGINGFACE_API_KEY='your-key-here'")
