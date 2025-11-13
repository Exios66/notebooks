"""
Comprehensive Models Registry
Contains full information and endpoints for publicly sourceable models
"""

from typing import Dict, List, Optional, Any
from dataclasses import dataclass, field
from enum import Enum


class ModelType(str, Enum):
    """Model type categories"""
    CHAT = "chat"
    INSTRUCT = "instruct"
    COMPLETION = "completion"
    EMBEDDING = "embedding"
    MULTIMODAL = "multimodal"


class AccessMethod(str, Enum):
    """Methods to access the model"""
    API = "api"
    LOCAL = "local"
    BOTH = "both"


class LicenseType(str, Enum):
    """License types for models"""
    APACHE_2 = "Apache-2.0"
    MIT = "MIT"
    BSD = "BSD"
    GPL = "GPL"
    PROPRIETARY = "Proprietary"
    CUSTOM = "Custom"
    OPEN_RAIL = "OpenRAIL"
    LLAMA2_COMMUNITY = "Llama 2 Community License"
    LLAMA3_COMMUNITY = "Llama 3 Community License"


@dataclass
class ModelEndpoint:
    """Model endpoint configuration"""
    url: str
    method: str = "POST"
    headers: Dict[str, str] = field(default_factory=dict)
    auth_required: bool = True
    rate_limit: Optional[str] = None


@dataclass
class ModelSpecs:
    """Model specifications"""
    parameters: Optional[int] = None  # Number of parameters in billions
    context_window: Optional[int] = None  # Context window size in tokens
    architecture: Optional[str] = None  # Model architecture
    quantization: Optional[List[str]] = None  # Available quantizations
    precision: Optional[List[str]] = None  # Available precisions (fp16, fp32, etc.)


@dataclass
class ModelInfo:
    """Complete model information"""
    model_id: str
    name: str
    provider: str
    type: ModelType
    access_method: AccessMethod
    description: str
    
    # Endpoints
    api_endpoint: Optional[ModelEndpoint] = None
    local_endpoint: Optional[str] = None  # HuggingFace model path for local loading
    
    # Specifications
    specs: Optional[ModelSpecs] = None
    
    # Licensing
    license: Optional[LicenseType] = None
    license_url: Optional[str] = None
    
    # Access requirements
    api_key_required: bool = True
    api_key_env_var: Optional[str] = None
    api_key_url: Optional[str] = None
    
    # Cost information
    cost_per_token: Optional[float] = None
    cost_per_1k_tokens: Optional[float] = None
    free_tier_available: bool = False
    free_tier_limits: Optional[str] = None
    
    # Usage information
    recommended_use_cases: List[str] = field(default_factory=list)
    limitations: List[str] = field(default_factory=list)
    
    # Additional metadata
    paper_url: Optional[str] = None
    github_url: Optional[str] = None
    documentation_url: Optional[str] = None
    model_card_url: Optional[str] = None
    
    # Technical details
    supported_languages: List[str] = field(default_factory=lambda: ["en"])
    max_output_tokens: Optional[int] = None
    default_temperature: float = 0.7
    default_max_tokens: int = 512


# HuggingFace Models Registry
HUGGINGFACE_MODELS: Dict[str, ModelInfo] = {
    "meta-llama/Llama-2-7b-chat-hf": ModelInfo(
        model_id="meta-llama/Llama-2-7b-chat-hf",
        name="Llama 2 7B Chat",
        provider="huggingface",
        type=ModelType.CHAT,
        access_method=AccessMethod.BOTH,
        description="Meta's Llama 2 7B chat model optimized for dialogue use cases",
        api_endpoint=ModelEndpoint(
            url="https://api-inference.huggingface.co/models/meta-llama/Llama-2-7b-chat-hf",
            method="POST",
            headers={"Content-Type": "application/json"},
            auth_required=True,
            rate_limit="30 requests/minute (free tier)"
        ),
        local_endpoint="meta-llama/Llama-2-7b-chat-hf",
        specs=ModelSpecs(
            parameters=7,
            context_window=4096,
            architecture="Transformer",
            quantization=["fp16", "int8", "int4"],
            precision=["fp32", "fp16"]
        ),
        license=LicenseType.LLAMA2_COMMUNITY,
        license_url="https://ai.meta.com/llama/license/",
        api_key_required=True,
        api_key_env_var="HUGGINGFACE_API_KEY",
        api_key_url="https://huggingface.co/settings/tokens",
        free_tier_available=True,
        free_tier_limits="30 requests/minute",
        recommended_use_cases=[
            "Conversational AI",
            "Customer support",
            "General Q&A",
            "Content generation"
        ],
        limitations=[
            "Requires HuggingFace account approval for gated models",
            "Context window limited to 4K tokens",
            "May require GPU for local inference"
        ],
        paper_url="https://arxiv.org/abs/2307.09288",
        documentation_url="https://huggingface.co/meta-llama/Llama-2-7b-chat-hf",
        model_card_url="https://huggingface.co/meta-llama/Llama-2-7b-chat-hf",
        supported_languages=["en", "es", "fr", "de", "it", "pt", "pl", "ru", "ja", "ko", "zh"],
        max_output_tokens=4096,
        default_temperature=0.7,
        default_max_tokens=512
    ),
    
    "meta-llama/Llama-2-13b-chat-hf": ModelInfo(
        model_id="meta-llama/Llama-2-13b-chat-hf",
        name="Llama 2 13B Chat",
        provider="huggingface",
        type=ModelType.CHAT,
        access_method=AccessMethod.BOTH,
        description="Meta's Llama 2 13B chat model with improved capabilities",
        api_endpoint=ModelEndpoint(
            url="https://api-inference.huggingface.co/models/meta-llama/Llama-2-13b-chat-hf",
            method="POST",
            headers={"Content-Type": "application/json"},
            auth_required=True,
            rate_limit="20 requests/minute (free tier)"
        ),
        local_endpoint="meta-llama/Llama-2-13b-chat-hf",
        specs=ModelSpecs(
            parameters=13,
            context_window=4096,
            architecture="Transformer",
            quantization=["fp16", "int8", "int4"],
            precision=["fp32", "fp16"]
        ),
        license=LicenseType.LLAMA2_COMMUNITY,
        license_url="https://ai.meta.com/llama/license/",
        api_key_required=True,
        api_key_env_var="HUGGINGFACE_API_KEY",
        api_key_url="https://huggingface.co/settings/tokens",
        free_tier_available=True,
        free_tier_limits="20 requests/minute",
        recommended_use_cases=[
            "Advanced conversational AI",
            "Complex reasoning tasks",
            "Multi-turn dialogues",
            "Technical Q&A"
        ],
        limitations=[
            "Requires HuggingFace account approval",
            "Larger model size requires more GPU memory",
            "Slower inference than 7B model"
        ],
        paper_url="https://arxiv.org/abs/2307.09288",
        documentation_url="https://huggingface.co/meta-llama/Llama-2-13b-chat-hf",
        model_card_url="https://huggingface.co/meta-llama/Llama-2-13b-chat-hf",
        supported_languages=["en", "es", "fr", "de", "it", "pt", "pl", "ru", "ja", "ko", "zh"],
        max_output_tokens=4096,
        default_temperature=0.7,
        default_max_tokens=512
    ),
    
    "meta-llama/Meta-Llama-3-8B-Instruct": ModelInfo(
        model_id="meta-llama/Meta-Llama-3-8B-Instruct",
        name="Llama 3 8B Instruct",
        provider="huggingface",
        type=ModelType.INSTRUCT,
        access_method=AccessMethod.BOTH,
        description="Meta's latest Llama 3 8B instruction-tuned model with improved performance",
        api_endpoint=ModelEndpoint(
            url="https://api-inference.huggingface.co/models/meta-llama/Meta-Llama-3-8B-Instruct",
            method="POST",
            headers={"Content-Type": "application/json"},
            auth_required=True,
            rate_limit="30 requests/minute (free tier)"
        ),
        local_endpoint="meta-llama/Meta-Llama-3-8B-Instruct",
        specs=ModelSpecs(
            parameters=8,
            context_window=8192,
            architecture="Transformer",
            quantization=["fp16", "int8", "int4"],
            precision=["fp32", "fp16"]
        ),
        license=LicenseType.LLAMA3_COMMUNITY,
        license_url="https://llama.meta.com/llama3/license/",
        api_key_required=True,
        api_key_env_var="HUGGINGFACE_API_KEY",
        api_key_url="https://huggingface.co/settings/tokens",
        free_tier_available=True,
        free_tier_limits="30 requests/minute",
        recommended_use_cases=[
            "Instruction following",
            "Code generation",
            "Reasoning tasks",
            "Multi-step problem solving"
        ],
        limitations=[
            "Requires HuggingFace account approval",
            "Newer model, may have less community support"
        ],
        paper_url="https://ai.meta.com/blog/meta-llama-3/",
        documentation_url="https://huggingface.co/meta-llama/Meta-Llama-3-8B-Instruct",
        model_card_url="https://huggingface.co/meta-llama/Meta-Llama-3-8B-Instruct",
        supported_languages=["en", "es", "fr", "de", "it", "pt", "pl", "ru", "ja", "ko", "zh"],
        max_output_tokens=8192,
        default_temperature=0.7,
        default_max_tokens=512
    ),
    
    "mistralai/Mistral-7B-Instruct-v0.2": ModelInfo(
        model_id="mistralai/Mistral-7B-Instruct-v0.2",
        name="Mistral 7B Instruct v0.2",
        provider="huggingface",
        type=ModelType.INSTRUCT,
        access_method=AccessMethod.BOTH,
        description="Mistral AI's 7B instruction-tuned model optimized for following instructions",
        api_endpoint=ModelEndpoint(
            url="https://api-inference.huggingface.co/models/mistralai/Mistral-7B-Instruct-v0.2",
            method="POST",
            headers={"Content-Type": "application/json"},
            auth_required=True,
            rate_limit="30 requests/minute (free tier)"
        ),
        local_endpoint="mistralai/Mistral-7B-Instruct-v0.2",
        specs=ModelSpecs(
            parameters=7,
            context_window=8192,
            architecture="Transformer",
            quantization=["fp16", "int8", "int4"],
            precision=["fp32", "fp16"]
        ),
        license=LicenseType.APACHE_2,
        license_url="https://www.apache.org/licenses/LICENSE-2.0",
        api_key_required=True,
        api_key_env_var="HUGGINGFACE_API_KEY",
        api_key_url="https://huggingface.co/settings/tokens",
        free_tier_available=True,
        free_tier_limits="30 requests/minute",
        recommended_use_cases=[
            "Instruction following",
            "Code generation",
            "Text summarization",
            "Question answering"
        ],
        limitations=[
            "May require GPU for optimal performance",
            "Context window limited to 8K tokens"
        ],
        paper_url="https://arxiv.org/abs/2310.06825",
        documentation_url="https://huggingface.co/mistralai/Mistral-7B-Instruct-v0.2",
        model_card_url="https://huggingface.co/mistralai/Mistral-7B-Instruct-v0.2",
        supported_languages=["en", "es", "fr", "de", "it"],
        max_output_tokens=8192,
        default_temperature=0.7,
        default_max_tokens=512
    ),
    
    "microsoft/DialoGPT-large": ModelInfo(
        model_id="microsoft/DialoGPT-large",
        name="DialoGPT Large",
        provider="huggingface",
        type=ModelType.CHAT,
        access_method=AccessMethod.BOTH,
        description="Microsoft's conversational AI model trained on Reddit dialogues",
        api_endpoint=ModelEndpoint(
            url="https://api-inference.huggingface.co/models/microsoft/DialoGPT-large",
            method="POST",
            headers={"Content-Type": "application/json"},
            auth_required=True,
            rate_limit="30 requests/minute (free tier)"
        ),
        local_endpoint="microsoft/DialoGPT-large",
        specs=ModelSpecs(
            parameters=0.774,  # 774M parameters
            context_window=1024,
            architecture="GPT-2 based",
            quantization=["fp16", "int8"],
            precision=["fp32", "fp16"]
        ),
        license=LicenseType.MIT,
        license_url="https://opensource.org/licenses/MIT",
        api_key_required=True,
        api_key_env_var="HUGGINGFACE_API_KEY",
        api_key_url="https://huggingface.co/settings/tokens",
        free_tier_available=True,
        free_tier_limits="30 requests/minute",
        recommended_use_cases=[
            "Casual conversation",
            "Chatbot applications",
            "Dialogue generation"
        ],
        limitations=[
            "Smaller context window (1K tokens)",
            "May generate repetitive responses",
            "Trained on Reddit data, may have biases"
        ],
        paper_url="https://arxiv.org/abs/1911.00536",
        documentation_url="https://huggingface.co/microsoft/DialoGPT-large",
        model_card_url="https://huggingface.co/microsoft/DialoGPT-large",
        supported_languages=["en"],
        max_output_tokens=1024,
        default_temperature=0.7,
        default_max_tokens=512
    ),
    
    "google/flan-t5-xxl": ModelInfo(
        model_id="google/flan-t5-xxl",
        name="FLAN-T5 XXL",
        provider="huggingface",
        type=ModelType.INSTRUCT,
        access_method=AccessMethod.BOTH,
        description="Google's instruction-tuned T5 model with 11B parameters",
        api_endpoint=ModelEndpoint(
            url="https://api-inference.huggingface.co/models/google/flan-t5-xxl",
            method="POST",
            headers={"Content-Type": "application/json"},
            auth_required=True,
            rate_limit="20 requests/minute (free tier)"
        ),
        local_endpoint="google/flan-t5-xxl",
        specs=ModelSpecs(
            parameters=11,
            context_window=512,
            architecture="T5 (Encoder-Decoder)",
            quantization=["fp16", "int8"],
            precision=["fp32", "fp16"]
        ),
        license=LicenseType.APACHE_2,
        license_url="https://www.apache.org/licenses/LICENSE-2.0",
        api_key_required=True,
        api_key_env_var="HUGGINGFACE_API_KEY",
        api_key_url="https://huggingface.co/settings/tokens",
        free_tier_available=True,
        free_tier_limits="20 requests/minute",
        recommended_use_cases=[
            "Instruction following",
            "Text summarization",
            "Question answering",
            "Translation"
        ],
        limitations=[
            "Smaller context window (512 tokens)",
            "Encoder-decoder architecture may be slower",
            "Requires significant GPU memory"
        ],
        paper_url="https://arxiv.org/abs/2210.11416",
        documentation_url="https://huggingface.co/google/flan-t5-xxl",
        model_card_url="https://huggingface.co/google/flan-t5-xxl",
        supported_languages=["en", "es", "fr", "de", "it", "pt", "ru", "zh", "ja"],
        max_output_tokens=512,
        default_temperature=0.7,
        default_max_tokens=256
    ),
    
    "HuggingFaceH4/zephyr-7b-beta": ModelInfo(
        model_id="HuggingFaceH4/zephyr-7b-beta",
        name="Zephyr 7B Beta",
        provider="huggingface",
        type=ModelType.INSTRUCT,
        access_method=AccessMethod.BOTH,
        description="HuggingFace's Zephyr instruction-tuned model based on Mistral 7B",
        api_endpoint=ModelEndpoint(
            url="https://api-inference.huggingface.co/models/HuggingFaceH4/zephyr-7b-beta",
            method="POST",
            headers={"Content-Type": "application/json"},
            auth_required=True,
            rate_limit="30 requests/minute (free tier)"
        ),
        local_endpoint="HuggingFaceH4/zephyr-7b-beta",
        specs=ModelSpecs(
            parameters=7,
            context_window=8192,
            architecture="Transformer",
            quantization=["fp16", "int8", "int4"],
            precision=["fp32", "fp16"]
        ),
        license=LicenseType.MIT,
        license_url="https://opensource.org/licenses/MIT",
        api_key_required=True,
        api_key_env_var="HUGGINGFACE_API_KEY",
        api_key_url="https://huggingface.co/settings/tokens",
        free_tier_available=True,
        free_tier_limits="30 requests/minute",
        recommended_use_cases=[
            "Instruction following",
            "Helpful assistant tasks",
            "Conversational AI",
            "General purpose tasks"
        ],
        limitations=[
            "Beta version, may have stability issues",
            "May require GPU for optimal performance"
        ],
        paper_url="https://huggingface.co/HuggingFaceH4/zephyr-7b-beta",
        documentation_url="https://huggingface.co/HuggingFaceH4/zephyr-7b-beta",
        model_card_url="https://huggingface.co/HuggingFaceH4/zephyr-7b-beta",
        supported_languages=["en"],
        max_output_tokens=8192,
        default_temperature=0.7,
        default_max_tokens=512
    ),
    
    "mistralai/Mixtral-8x7B-Instruct-v0.1": ModelInfo(
        model_id="mistralai/Mixtral-8x7B-Instruct-v0.1",
        name="Mixtral 8x7B Instruct",
        provider="huggingface",
        type=ModelType.INSTRUCT,
        access_method=AccessMethod.BOTH,
        description="Mistral AI's mixture of experts model with 8x7B parameters",
        api_endpoint=ModelEndpoint(
            url="https://api-inference.huggingface.co/models/mistralai/Mixtral-8x7B-Instruct-v0.1",
            method="POST",
            headers={"Content-Type": "application/json"},
            auth_required=True,
            rate_limit="10 requests/minute (free tier)"
        ),
        local_endpoint="mistralai/Mixtral-8x7B-Instruct-v0.1",
        specs=ModelSpecs(
            parameters=47,  # 8x7B with sparse activation
            context_window=32768,
            architecture="Mixture of Experts (MoE)",
            quantization=["fp16", "int8", "int4"],
            precision=["fp32", "fp16"]
        ),
        license=LicenseType.APACHE_2,
        license_url="https://www.apache.org/licenses/LICENSE-2.0",
        api_key_required=True,
        api_key_env_var="HUGGINGFACE_API_KEY",
        api_key_url="https://huggingface.co/settings/tokens",
        free_tier_available=True,
        free_tier_limits="10 requests/minute",
        recommended_use_cases=[
            "Complex reasoning",
            "Code generation",
            "Long context tasks",
            "Multi-step problem solving"
        ],
        limitations=[
            "Requires significant GPU memory",
            "Slower inference than single-expert models",
            "Higher API rate limits"
        ],
        paper_url="https://arxiv.org/abs/2401.04088",
        documentation_url="https://huggingface.co/mistralai/Mixtral-8x7B-Instruct-v0.1",
        model_card_url="https://huggingface.co/mistralai/Mixtral-8x7B-Instruct-v0.1",
        supported_languages=["en", "es", "fr", "de", "it"],
        max_output_tokens=32768,
        default_temperature=0.7,
        default_max_tokens=512
    ),
    
    "Qwen/Qwen2.5-7B-Instruct": ModelInfo(
        model_id="Qwen/Qwen2.5-7B-Instruct",
        name="Qwen 2.5 7B Instruct",
        provider="huggingface",
        type=ModelType.INSTRUCT,
        access_method=AccessMethod.BOTH,
        description="Alibaba's Qwen 2.5 7B instruction-tuned model with strong multilingual support",
        api_endpoint=ModelEndpoint(
            url="https://api-inference.huggingface.co/models/Qwen/Qwen2.5-7B-Instruct",
            method="POST",
            headers={"Content-Type": "application/json"},
            auth_required=True,
            rate_limit="30 requests/minute (free tier)"
        ),
        local_endpoint="Qwen/Qwen2.5-7B-Instruct",
        specs=ModelSpecs(
            parameters=7,
            context_window=32768,
            architecture="Transformer",
            quantization=["fp16", "int8", "int4"],
            precision=["fp32", "fp16"]
        ),
        license=LicenseType.APACHE_2,
        license_url="https://www.apache.org/licenses/LICENSE-2.0",
        api_key_required=True,
        api_key_env_var="HUGGINGFACE_API_KEY",
        api_key_url="https://huggingface.co/settings/tokens",
        free_tier_available=True,
        free_tier_limits="30 requests/minute",
        recommended_use_cases=[
            "Multilingual tasks",
            "Code generation",
            "Reasoning tasks",
            "Long context processing"
        ],
        limitations=[
            "May require GPU for optimal performance",
            "Newer model, less community support"
        ],
        paper_url="https://qwenlm.github.io/blog/qwen2.5/",
        documentation_url="https://huggingface.co/Qwen/Qwen2.5-7B-Instruct",
        model_card_url="https://huggingface.co/Qwen/Qwen2.5-7B-Instruct",
        supported_languages=["en", "zh", "es", "fr", "de", "it", "pt", "ru", "ja", "ko", "ar", "hi"],
        max_output_tokens=32768,
        default_temperature=0.7,
        default_max_tokens=512
    ),
    
    "google/gemma-7b-it": ModelInfo(
        model_id="google/gemma-7b-it",
        name="Gemma 7B Instruct",
        provider="huggingface",
        type=ModelType.INSTRUCT,
        access_method=AccessMethod.BOTH,
        description="Google's Gemma 7B instruction-tuned model based on Gemini technology",
        api_endpoint=ModelEndpoint(
            url="https://api-inference.huggingface.co/models/google/gemma-7b-it",
            method="POST",
            headers={"Content-Type": "application/json"},
            auth_required=True,
            rate_limit="30 requests/minute (free tier)"
        ),
        local_endpoint="google/gemma-7b-it",
        specs=ModelSpecs(
            parameters=7,
            context_window=8192,
            architecture="Transformer",
            quantization=["fp16", "int8", "int4"],
            precision=["fp32", "fp16"]
        ),
        license=LicenseType.CUSTOM,
        license_url="https://ai.google.dev/gemma/terms",
        api_key_required=True,
        api_key_env_var="HUGGINGFACE_API_KEY",
        api_key_url="https://huggingface.co/settings/tokens",
        free_tier_available=True,
        free_tier_limits="30 requests/minute",
        recommended_use_cases=[
            "Instruction following",
            "Text generation",
            "Question answering",
            "Code generation"
        ],
        limitations=[
            "Custom license terms apply",
            "May require GPU for optimal performance"
        ],
        paper_url="https://ai.google.dev/gemma",
        documentation_url="https://huggingface.co/google/gemma-7b-it",
        model_card_url="https://huggingface.co/google/gemma-7b-it",
        supported_languages=["en", "es", "fr", "de", "it", "pt", "ru", "ja", "ko", "zh"],
        max_output_tokens=8192,
        default_temperature=0.7,
        default_max_tokens=512
    ),
}


# OpenAI Models Registry
OPENAI_MODELS: Dict[str, ModelInfo] = {
    "gpt-4": ModelInfo(
        model_id="gpt-4",
        name="GPT-4",
        provider="openai",
        type=ModelType.CHAT,
        access_method=AccessMethod.API,
        description="OpenAI's most capable model with advanced reasoning capabilities",
        api_endpoint=ModelEndpoint(
            url="https://api.openai.com/v1/chat/completions",
            method="POST",
            headers={"Content-Type": "application/json"},
            auth_required=True,
            rate_limit="Varies by tier (500-10,000 requests/minute)"
        ),
        specs=ModelSpecs(
            parameters=None,  # Not publicly disclosed
            context_window=8192,
            architecture="Transformer (proprietary)",
            precision=["fp16"]
        ),
        license=LicenseType.PROPRIETARY,
        license_url="https://openai.com/policies/terms-of-use",
        api_key_required=True,
        api_key_env_var="OPENAI_API_KEY",
        api_key_url="https://platform.openai.com/api-keys",
        cost_per_1k_tokens=0.03,  # Approximate for input tokens
        free_tier_available=False,
        recommended_use_cases=[
            "Complex reasoning",
            "Code generation",
            "Creative writing",
            "Analysis and synthesis",
            "Advanced Q&A"
        ],
        limitations=[
            "Proprietary model, no local access",
            "Requires paid API access",
            "Rate limits apply",
            "Context window limited to 8K tokens"
        ],
        documentation_url="https://platform.openai.com/docs/models/gpt-4",
        supported_languages=["en", "es", "fr", "de", "it", "pt", "ru", "ja", "ko", "zh", "ar", "hi"],
        max_output_tokens=8192,
        default_temperature=0.7,
        default_max_tokens=512
    ),
    
    "gpt-4-turbo": ModelInfo(
        model_id="gpt-4-turbo",
        name="GPT-4 Turbo",
        provider="openai",
        type=ModelType.CHAT,
        access_method=AccessMethod.API,
        description="Faster and more capable GPT-4 variant with extended context window",
        api_endpoint=ModelEndpoint(
            url="https://api.openai.com/v1/chat/completions",
            method="POST",
            headers={"Content-Type": "application/json"},
            auth_required=True,
            rate_limit="Varies by tier (500-10,000 requests/minute)"
        ),
        specs=ModelSpecs(
            parameters=None,
            context_window=128000,
            architecture="Transformer (proprietary)",
            precision=["fp16"]
        ),
        license=LicenseType.PROPRIETARY,
        license_url="https://openai.com/policies/terms-of-use",
        api_key_required=True,
        api_key_env_var="OPENAI_API_KEY",
        api_key_url="https://platform.openai.com/api-keys",
        cost_per_1k_tokens=0.01,  # Approximate for input tokens
        free_tier_available=False,
        recommended_use_cases=[
            "Long context processing",
            "Document analysis",
            "Code generation",
            "Complex reasoning",
            "Multimodal tasks"
        ],
        limitations=[
            "Proprietary model",
            "Requires paid API access",
            "Higher cost than GPT-3.5"
        ],
        documentation_url="https://platform.openai.com/docs/models/gpt-4-turbo",
        supported_languages=["en", "es", "fr", "de", "it", "pt", "ru", "ja", "ko", "zh", "ar", "hi"],
        max_output_tokens=16384,
        default_temperature=0.7,
        default_max_tokens=4096
    ),
    
    "gpt-4-turbo-preview": ModelInfo(
        model_id="gpt-4-turbo-preview",
        name="GPT-4 Turbo Preview",
        provider="openai",
        type=ModelType.CHAT,
        access_method=AccessMethod.API,
        description="Preview version of GPT-4 Turbo with latest improvements",
        api_endpoint=ModelEndpoint(
            url="https://api.openai.com/v1/chat/completions",
            method="POST",
            headers={"Content-Type": "application/json"},
            auth_required=True,
            rate_limit="Varies by tier"
        ),
        specs=ModelSpecs(
            parameters=None,
            context_window=128000,
            architecture="Transformer (proprietary)",
            precision=["fp16"]
        ),
        license=LicenseType.PROPRIETARY,
        license_url="https://openai.com/policies/terms-of-use",
        api_key_required=True,
        api_key_env_var="OPENAI_API_KEY",
        api_key_url="https://platform.openai.com/api-keys",
        cost_per_1k_tokens=0.01,
        free_tier_available=False,
        recommended_use_cases=[
            "Testing new features",
            "Long context tasks",
            "Advanced reasoning"
        ],
        limitations=[
            "Preview version, may change",
            "Proprietary model",
            "Requires paid access"
        ],
        documentation_url="https://platform.openai.com/docs/models/gpt-4-turbo",
        supported_languages=["en", "es", "fr", "de", "it", "pt", "ru", "ja", "ko", "zh"],
        max_output_tokens=16384,
        default_temperature=0.7,
        default_max_tokens=4096
    ),
    
    "gpt-3.5-turbo": ModelInfo(
        model_id="gpt-3.5-turbo",
        name="GPT-3.5 Turbo",
        provider="openai",
        type=ModelType.CHAT,
        access_method=AccessMethod.API,
        description="Fast and efficient GPT-3.5 model optimized for speed and cost",
        api_endpoint=ModelEndpoint(
            url="https://api.openai.com/v1/chat/completions",
            method="POST",
            headers={"Content-Type": "application/json"},
            auth_required=True,
            rate_limit="Varies by tier (3,500-10,000 requests/minute)"
        ),
        specs=ModelSpecs(
            parameters=None,
            context_window=16385,
            architecture="Transformer (proprietary)",
            precision=["fp16"]
        ),
        license=LicenseType.PROPRIETARY,
        license_url="https://openai.com/policies/terms-of-use",
        api_key_required=True,
        api_key_env_var="OPENAI_API_KEY",
        api_key_url="https://platform.openai.com/api-keys",
        cost_per_1k_tokens=0.0005,  # Approximate for input tokens
        free_tier_available=False,
        recommended_use_cases=[
            "General purpose chat",
            "Quick responses",
            "Cost-effective applications",
            "High-volume tasks"
        ],
        limitations=[
            "Proprietary model",
            "Requires paid API access",
            "Less capable than GPT-4"
        ],
        documentation_url="https://platform.openai.com/docs/models/gpt-3-5-turbo",
        supported_languages=["en", "es", "fr", "de", "it", "pt", "ru", "ja", "ko", "zh"],
        max_output_tokens=16385,
        default_temperature=0.7,
        default_max_tokens=4096
    ),
    
    "gpt-3.5-turbo-16k": ModelInfo(
        model_id="gpt-3.5-turbo-16k",
        name="GPT-3.5 Turbo 16K",
        provider="openai",
        type=ModelType.CHAT,
        access_method=AccessMethod.API,
        description="GPT-3.5 Turbo with extended 16K context window",
        api_endpoint=ModelEndpoint(
            url="https://api.openai.com/v1/chat/completions",
            method="POST",
            headers={"Content-Type": "application/json"},
            auth_required=True,
            rate_limit="Varies by tier"
        ),
        specs=ModelSpecs(
            parameters=None,
            context_window=16385,
            architecture="Transformer (proprietary)",
            precision=["fp16"]
        ),
        license=LicenseType.PROPRIETARY,
        license_url="https://openai.com/policies/terms-of-use",
        api_key_required=True,
        api_key_env_var="OPENAI_API_KEY",
        api_key_url="https://platform.openai.com/api-keys",
        cost_per_1k_tokens=0.003,  # Approximate for input tokens
        free_tier_available=False,
        recommended_use_cases=[
            "Long documents",
            "Extended conversations",
            "Context-heavy tasks"
        ],
        limitations=[
            "Proprietary model",
            "Requires paid access",
            "Higher cost than standard GPT-3.5"
        ],
        documentation_url="https://platform.openai.com/docs/models/gpt-3-5-turbo",
        supported_languages=["en", "es", "fr", "de", "it", "pt", "ru", "ja", "ko", "zh"],
        max_output_tokens=16385,
        default_temperature=0.7,
        default_max_tokens=4096
    ),
    
    "gpt-4o": ModelInfo(
        model_id="gpt-4o",
        name="GPT-4o",
        provider="openai",
        type=ModelType.MULTIMODAL,
        access_method=AccessMethod.API,
        description="OpenAI's latest multimodal model optimized for speed and cost",
        api_endpoint=ModelEndpoint(
            url="https://api.openai.com/v1/chat/completions",
            method="POST",
            headers={"Content-Type": "application/json"},
            auth_required=True,
            rate_limit="Varies by tier"
        ),
        specs=ModelSpecs(
            parameters=None,
            context_window=128000,
            architecture="Transformer (proprietary)",
            precision=["fp16"]
        ),
        license=LicenseType.PROPRIETARY,
        license_url="https://openai.com/policies/terms-of-use",
        api_key_required=True,
        api_key_env_var="OPENAI_API_KEY",
        api_key_url="https://platform.openai.com/api-keys",
        cost_per_1k_tokens=0.005,  # Approximate for input tokens
        free_tier_available=False,
        recommended_use_cases=[
            "Multimodal tasks",
            "Vision and text",
            "Fast responses",
            "Cost-effective advanced tasks"
        ],
        limitations=[
            "Proprietary model",
            "Requires paid access",
            "Newer model, may have less documentation"
        ],
        documentation_url="https://platform.openai.com/docs/models/gpt-4o",
        supported_languages=["en", "es", "fr", "de", "it", "pt", "ru", "ja", "ko", "zh", "ar", "hi"],
        max_output_tokens=16384,
        default_temperature=0.7,
        default_max_tokens=4096
    ),
    
    "gpt-4o-mini": ModelInfo(
        model_id="gpt-4o-mini",
        name="GPT-4o Mini",
        provider="openai",
        type=ModelType.MULTIMODAL,
        access_method=AccessMethod.API,
        description="Smaller, faster, and more affordable version of GPT-4o",
        api_endpoint=ModelEndpoint(
            url="https://api.openai.com/v1/chat/completions",
            method="POST",
            headers={"Content-Type": "application/json"},
            auth_required=True,
            rate_limit="Varies by tier"
        ),
        specs=ModelSpecs(
            parameters=None,
            context_window=128000,
            architecture="Transformer (proprietary)",
            precision=["fp16"]
        ),
        license=LicenseType.PROPRIETARY,
        license_url="https://openai.com/policies/terms-of-use",
        api_key_required=True,
        api_key_env_var="OPENAI_API_KEY",
        api_key_url="https://platform.openai.com/api-keys",
        cost_per_1k_tokens=0.00015,  # Approximate for input tokens
        free_tier_available=False,
        recommended_use_cases=[
            "Cost-effective multimodal tasks",
            "High-volume applications",
            "Quick responses",
            "General purpose chat"
        ],
        limitations=[
            "Proprietary model",
            "Requires paid access",
            "Less capable than GPT-4o"
        ],
        documentation_url="https://platform.openai.com/docs/models/gpt-4o-mini",
        supported_languages=["en", "es", "fr", "de", "it", "pt", "ru", "ja", "ko", "zh"],
        max_output_tokens=16384,
        default_temperature=0.7,
        default_max_tokens=4096
    ),
}


# Combined registry
ALL_MODELS: Dict[str, ModelInfo] = {**HUGGINGFACE_MODELS, **OPENAI_MODELS}


def get_model_info(model_id: str) -> Optional[ModelInfo]:
    """Get model information by model ID"""
    return ALL_MODELS.get(model_id)


def list_models_by_provider(provider: str) -> List[ModelInfo]:
    """List all models for a specific provider"""
    if provider.lower() == "huggingface":
        return list(HUGGINGFACE_MODELS.values())
    elif provider.lower() == "openai":
        return list(OPENAI_MODELS.values())
    else:
        return []


def list_models_by_type(model_type: ModelType) -> List[ModelInfo]:
    """List all models of a specific type"""
    return [model for model in ALL_MODELS.values() if model.type == model_type]


def search_models(query: str) -> List[ModelInfo]:
    """Search models by name, description, or use case"""
    query_lower = query.lower()
    results = []
    for model in ALL_MODELS.values():
        if (query_lower in model.name.lower() or
            query_lower in model.description.lower() or
            any(query_lower in use_case.lower() for use_case in model.recommended_use_cases)):
            results.append(model)
    return results


def get_free_models() -> List[ModelInfo]:
    """Get all models with free tier available"""
    return [model for model in ALL_MODELS.values() if model.free_tier_available]


def get_local_models() -> List[ModelInfo]:
    """Get all models that can be run locally"""
    return [model for model in ALL_MODELS.values() 
            if model.access_method in [AccessMethod.LOCAL, AccessMethod.BOTH]]


def export_to_dict() -> Dict[str, Dict[str, Any]]:
    """Export all models to a dictionary format"""
    result = {}
    for model_id, model_info in ALL_MODELS.items():
        result[model_id] = {
            "model_id": model_info.model_id,
            "name": model_info.name,
            "provider": model_info.provider,
            "type": model_info.type.value,
            "access_method": model_info.access_method.value,
            "description": model_info.description,
            "api_endpoint": {
                "url": model_info.api_endpoint.url if model_info.api_endpoint else None,
                "method": model_info.api_endpoint.method if model_info.api_endpoint else None,
                "auth_required": model_info.api_endpoint.auth_required if model_info.api_endpoint else None,
                "rate_limit": model_info.api_endpoint.rate_limit if model_info.api_endpoint else None,
            } if model_info.api_endpoint else None,
            "local_endpoint": model_info.local_endpoint,
            "specs": {
                "parameters": model_info.specs.parameters if model_info.specs else None,
                "context_window": model_info.specs.context_window if model_info.specs else None,
                "architecture": model_info.specs.architecture if model_info.specs else None,
            } if model_info.specs else None,
            "license": model_info.license.value if model_info.license else None,
            "license_url": model_info.license_url,
            "api_key_required": model_info.api_key_required,
            "api_key_env_var": model_info.api_key_env_var,
            "api_key_url": model_info.api_key_url,
            "cost_per_1k_tokens": model_info.cost_per_1k_tokens,
            "free_tier_available": model_info.free_tier_available,
            "free_tier_limits": model_info.free_tier_limits,
            "recommended_use_cases": model_info.recommended_use_cases,
            "limitations": model_info.limitations,
            "documentation_url": model_info.documentation_url,
            "model_card_url": model_info.model_card_url,
            "supported_languages": model_info.supported_languages,
            "max_output_tokens": model_info.max_output_tokens,
            "default_temperature": model_info.default_temperature,
            "default_max_tokens": model_info.default_max_tokens,
        }
    return result

