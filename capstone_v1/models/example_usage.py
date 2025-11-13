"""
Example usage of the Models Registry

This script demonstrates how to use the comprehensive models registry
to access full information and endpoints for publicly sourceable models.
"""

from models_registry import (
    get_model_info,
    list_models_by_provider,
    list_models_by_type,
    search_models,
    get_free_models,
    get_local_models,
    ModelType,
    ALL_MODELS,
)


def example_get_model_info():
    """Example: Get detailed information about a specific model"""
    print("=" * 60)
    print("Example: Get Model Information")
    print("=" * 60)
    
    model_id = "gpt-3.5-turbo"
    model_info = get_model_info(model_id)
    
    if model_info:
        print(f"\nModel: {model_info.name}")
        print(f"Provider: {model_info.provider}")
        print(f"Type: {model_info.type.value}")
        print(f"Description: {model_info.description}")
        print(f"\nAPI Endpoint: {model_info.api_endpoint.url if model_info.api_endpoint else 'N/A'}")
        print(f"Rate Limit: {model_info.api_endpoint.rate_limit if model_info.api_endpoint else 'N/A'}")
        print(f"\nSpecifications:")
        if model_info.specs:
            print(f"  Parameters: {model_info.specs.parameters}B" if model_info.specs.parameters else "  Parameters: Not disclosed")
            print(f"  Context Window: {model_info.specs.context_window:,} tokens")
        print(f"\nCost: ${model_info.cost_per_1k_tokens}/1K tokens" if model_info.cost_per_1k_tokens else "\nCost: Free tier available" if model_info.free_tier_available else "\nCost: Paid API")
        print(f"\nRecommended Use Cases:")
        for use_case in model_info.recommended_use_cases:
            print(f"  - {use_case}")
        print(f"\nLimitations:")
        for limitation in model_info.limitations:
            print(f"  - {limitation}")
    else:
        print(f"Model '{model_id}' not found in registry")


def example_list_models():
    """Example: List models by provider"""
    print("\n" + "=" * 60)
    print("Example: List Models by Provider")
    print("=" * 60)
    
    print("\nHuggingFace Models:")
    hf_models = list_models_by_provider("huggingface")
    for model in hf_models[:5]:  # Show first 5
        print(f"  - {model.model_id}: {model.name}")
    print(f"  ... and {len(hf_models) - 5} more")
    
    print("\nOpenAI Models:")
    openai_models = list_models_by_provider("openai")
    for model in openai_models:
        print(f"  - {model.model_id}: {model.name}")


def example_search_models():
    """Example: Search for models"""
    print("\n" + "=" * 60)
    print("Example: Search Models")
    print("=" * 60)
    
    query = "instruction"
    results = search_models(query)
    
    print(f"\nSearch results for '{query}':")
    for model in results:
        print(f"  - {model.model_id}: {model.name}")
        print(f"    {model.description[:80]}...")


def example_free_models():
    """Example: Get free tier models"""
    print("\n" + "=" * 60)
    print("Example: Free Tier Models")
    print("=" * 60)
    
    free_models = get_free_models()
    print(f"\nFound {len(free_models)} models with free tier:")
    for model in free_models:
        print(f"  - {model.model_id}: {model.name}")
        print(f"    Free Tier: {model.free_tier_limits}")


def example_local_models():
    """Example: Get models that can run locally"""
    print("\n" + "=" * 60)
    print("Example: Local Models")
    print("=" * 60)
    
    local_models = get_local_models()
    print(f"\nFound {len(local_models)} models that can run locally:")
    for model in local_models[:5]:  # Show first 5
        print(f"  - {model.model_id}: {model.name}")
        print(f"    Local Endpoint: {model.local_endpoint}")
    print(f"  ... and {len(local_models) - 5} more")


def example_model_comparison():
    """Example: Compare models by type"""
    print("\n" + "=" * 60)
    print("Example: Compare Models by Type")
    print("=" * 60)
    
    chat_models = list_models_by_type(ModelType.CHAT)
    instruct_models = list_models_by_type(ModelType.INSTRUCT)
    
    print(f"\nChat Models: {len(chat_models)}")
    for model in chat_models[:3]:
        print(f"  - {model.name} ({model.provider})")
    
    print(f"\nInstruct Models: {len(instruct_models)}")
    for model in instruct_models[:3]:
        print(f"  - {model.name} ({model.provider})")


def example_endpoint_info():
    """Example: Get endpoint information for API access"""
    print("\n" + "=" * 60)
    print("Example: API Endpoint Information")
    print("=" * 60)
    
    model_id = "meta-llama/Llama-2-7b-chat-hf"
    model_info = get_model_info(model_id)
    
    if model_info and model_info.api_endpoint:
        print(f"\nModel: {model_info.name}")
        print(f"API Endpoint: {model_info.api_endpoint.url}")
        print(f"Method: {model_info.api_endpoint.method}")
        print(f"Auth Required: {model_info.api_endpoint.auth_required}")
        print(f"Rate Limit: {model_info.api_endpoint.rate_limit}")
        print(f"\nAPI Key Required: {model_info.api_key_required}")
        if model_info.api_key_required:
            print(f"API Key Env Var: {model_info.api_key_env_var}")
            print(f"Get API Key: {model_info.api_key_url}")


def example_use_cases():
    """Example: Find models for specific use cases"""
    print("\n" + "=" * 60)
    print("Example: Find Models for Use Cases")
    print("=" * 60)
    
    # Find models good for code generation
    code_models = [m for m in ALL_MODELS.values() 
                   if "code" in " ".join(m.recommended_use_cases).lower()]
    
    print("\nModels recommended for code generation:")
    for model in code_models:
        print(f"  - {model.name} ({model.provider})")
        print(f"    Use cases: {', '.join([uc for uc in model.recommended_use_cases if 'code' in uc.lower()])}")


if __name__ == "__main__":
    print("\n" + "=" * 60)
    print("Models Registry - Usage Examples")
    print("=" * 60)
    
    example_get_model_info()
    example_list_models()
    example_search_models()
    example_free_models()
    example_local_models()
    example_model_comparison()
    example_endpoint_info()
    example_use_cases()
    
    print("\n" + "=" * 60)
    print(f"Total models in registry: {len(ALL_MODELS)}")
    print("=" * 60 + "\n")

