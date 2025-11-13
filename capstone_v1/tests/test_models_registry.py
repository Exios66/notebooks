"""
Unit tests for Models Registry
"""

import pytest
from models.models_registry import (
    get_model_info,
    list_models_by_provider,
    list_models_by_type,
    search_models,
    get_free_models,
    get_local_models,
    ModelType,
    AccessMethod,
    ALL_MODELS,
    HUGGINGFACE_MODELS,
    OPENAI_MODELS,
)


class TestModelsRegistry:
    """Test cases for Models Registry"""
    
    def test_get_model_info_existing(self):
        """Test getting information for existing models"""
        # Test OpenAI model
        model_info = get_model_info("gpt-3.5-turbo")
        assert model_info is not None
        assert model_info.model_id == "gpt-3.5-turbo"
        assert model_info.provider == "openai"
        
        # Test HuggingFace model
        model_info = get_model_info("meta-llama/Llama-2-7b-chat-hf")
        assert model_info is not None
        assert model_info.provider == "huggingface"
    
    def test_get_model_info_nonexistent(self):
        """Test getting information for non-existent model"""
        model_info = get_model_info("nonexistent-model")
        assert model_info is None
    
    def test_list_models_by_provider(self):
        """Test listing models by provider"""
        hf_models = list_models_by_provider("huggingface")
        assert len(hf_models) > 0
        assert all(m.provider == "huggingface" for m in hf_models)
        
        openai_models = list_models_by_provider("openai")
        assert len(openai_models) > 0
        assert all(m.provider == "openai" for m in openai_models)
    
    def test_list_models_by_type(self):
        """Test listing models by type"""
        chat_models = list_models_by_type(ModelType.CHAT)
        assert len(chat_models) > 0
        assert all(m.type == ModelType.CHAT for m in chat_models)
        
        instruct_models = list_models_by_type(ModelType.INSTRUCT)
        assert len(instruct_models) > 0
        assert all(m.type == ModelType.INSTRUCT for m in instruct_models)
    
    def test_search_models(self):
        """Test searching models"""
        results = search_models("instruction")
        assert len(results) > 0
        # All results should contain "instruction" in name, description, or use cases
        for model in results:
            assert (
                "instruction" in model.name.lower() or
                "instruction" in model.description.lower() or
                any("instruction" in uc.lower() for uc in model.recommended_use_cases)
            )
    
    def test_get_free_models(self):
        """Test getting free tier models"""
        free_models = get_free_models()
        assert len(free_models) > 0
        assert all(m.free_tier_available for m in free_models)
    
    def test_get_local_models(self):
        """Test getting local models"""
        local_models = get_local_models()
        assert len(local_models) > 0
        assert all(
            m.access_method in [AccessMethod.LOCAL, AccessMethod.BOTH]
            for m in local_models
        )
    
    def test_model_info_structure(self):
        """Test that model info has required fields"""
        model_info = get_model_info("gpt-3.5-turbo")
        assert model_info is not None
        
        # Required fields
        assert hasattr(model_info, "model_id")
        assert hasattr(model_info, "name")
        assert hasattr(model_info, "provider")
        assert hasattr(model_info, "type")
        assert hasattr(model_info, "description")
        assert hasattr(model_info, "access_method")
    
    def test_api_endpoint_structure(self):
        """Test API endpoint structure"""
        model_info = get_model_info("gpt-3.5-turbo")
        if model_info and model_info.api_endpoint:
            assert hasattr(model_info.api_endpoint, "url")
            assert hasattr(model_info.api_endpoint, "method")
            assert hasattr(model_info.api_endpoint, "auth_required")
    
    def test_all_models_count(self):
        """Test that all models are included"""
        assert len(ALL_MODELS) == len(HUGGINGFACE_MODELS) + len(OPENAI_MODELS)
        assert len(ALL_MODELS) > 0
    
    def test_model_specs(self):
        """Test model specifications"""
        model_info = get_model_info("gpt-3.5-turbo")
        if model_info and model_info.specs:
            # Specs should have context_window if available
            assert hasattr(model_info.specs, "context_window")
    
    def test_export_to_dict(self):
        """Test exporting to dictionary"""
        from models.models_registry import export_to_dict
        data = export_to_dict()
        assert isinstance(data, dict)
        assert len(data) == len(ALL_MODELS)
        assert "gpt-3.5-turbo" in data
        assert isinstance(data["gpt-3.5-turbo"], dict)

