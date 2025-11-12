"""
HuggingFace API Client for chatbot interactions
Supports both Inference API and local model loading
"""

import os
import requests
import json
from typing import Dict, List, Optional, Union, Any
from transformers import AutoTokenizer, AutoModelForCausalLM, pipeline
import torch

from .config import (
    HUGGINGFACE_API_KEY,
    HUGGINGFACE_API_URL,
    DEFAULT_TEMPERATURE,
    DEFAULT_MAX_TOKENS,
    DEFAULT_TOP_P,
    DEFAULT_TOP_K,
)


class HuggingFaceClient:
    """
    Client for interacting with HuggingFace models via Inference API or locally
    """

    def __init__(
        self,
        api_key: Optional[str] = None,
        use_local: bool = False,
        device: str = "auto",
    ):
        """
        Initialize HuggingFace client

        Args:
            api_key: HuggingFace API key (if None, uses HUGGINGFACE_API_KEY env var)
            use_local: If True, load models locally instead of using Inference API
            device: Device to use for local models ('cpu', 'cuda', 'auto')
        """
        self.api_key = api_key or HUGGINGFACE_API_KEY
        self.use_local = use_local
        self.device = device
        self.base_url = HUGGINGFACE_API_URL
        self.local_models: Dict[str, Any] = {}
        self.local_tokenizers: Dict[str, Any] = {}

        if self.use_local:
            # Determine device
            if device == "auto":
                self.device = "cuda" if torch.cuda.is_available() else "cpu"
            else:
                self.device = device

    def _get_headers(self) -> Dict[str, str]:
        """Get headers for API requests"""
        headers = {"Content-Type": "application/json"}
        if self.api_key:
            headers["Authorization"] = f"Bearer {self.api_key}"
        return headers

    def _load_model_locally(self, model_id: str) -> tuple:
        """
        Load a model and tokenizer locally

        Args:
            model_id: HuggingFace model identifier

        Returns:
            Tuple of (model, tokenizer)
        """
        if model_id in self.local_models:
            return self.local_models[model_id], self.local_tokenizers[model_id]

        print(f"Loading model {model_id} locally...")
        try:
            tokenizer = AutoTokenizer.from_pretrained(model_id)
            model = AutoModelForCausalLM.from_pretrained(
                model_id,
                torch_dtype=torch.float16 if self.device == "cuda" else torch.float32,
                device_map="auto" if self.device == "cuda" else None,
            )

            if self.device == "cpu":
                model = model.to(self.device)

            self.local_tokenizers[model_id] = tokenizer
            self.local_models[model_id] = model
            return model, tokenizer
        except Exception as e:
            raise Exception(f"Failed to load model {model_id}: {str(e)}")

    def chat(
        self,
        model_id: str,
        messages: Union[str, List[Dict[str, str]]],
        temperature: float = DEFAULT_TEMPERATURE,
        max_tokens: int = DEFAULT_MAX_TOKENS,
        top_p: float = DEFAULT_TOP_P,
        top_k: int = DEFAULT_TOP_K,
        **kwargs,
    ) -> Dict[str, Any]:
        """
        Generate a chat response using HuggingFace model

        Args:
            model_id: HuggingFace model identifier
            messages: Either a string prompt or list of message dicts with 'role' and 'content'
            temperature: Sampling temperature (0.0 to 1.0)
            max_tokens: Maximum tokens to generate
            top_p: Nucleus sampling parameter
            top_k: Top-k sampling parameter
            **kwargs: Additional parameters

        Returns:
            Dictionary with 'response' and metadata
        """
        if self.use_local:
            return self._chat_local(
                model_id, messages, temperature, max_tokens, top_p, top_k, **kwargs
            )
        else:
            return self._chat_api(
                model_id, messages, temperature, max_tokens, top_p, top_k, **kwargs
            )

    def _chat_api(
        self,
        model_id: str,
        messages: Union[str, List[Dict[str, str]]],
        temperature: float,
        max_tokens: int,
        top_p: float,
        top_k: int,
        **kwargs,
    ) -> Dict[str, Any]:
        """Generate response using HuggingFace Inference API"""
        url = f"{self.base_url}/{model_id}"

        # Format messages
        if isinstance(messages, str):
            prompt = messages
        else:
            # Convert message list to prompt
            prompt = self._format_messages(messages)

        # Prepare request payload
        payload = {
            "inputs": prompt,
            "parameters": {
                "temperature": temperature,
                "max_new_tokens": max_tokens,
                "top_p": top_p,
                "top_k": top_k,
                "return_full_text": False,
                **kwargs,
            },
        }

        try:
            response = requests.post(
                url, headers=self._get_headers(), json=payload, timeout=120
            )
            response.raise_for_status()

            result = response.json()

            # Handle different response formats
            if isinstance(result, list) and len(result) > 0:
                generated_text = result[0].get("generated_text", "")
            elif isinstance(result, dict):
                generated_text = result.get("generated_text", "")
            else:
                generated_text = str(result)

            return {
                "response": generated_text.strip(),
                "model": model_id,
                "provider": "huggingface",
                "method": "api",
            }
        except requests.exceptions.RequestException as e:
            raise Exception(f"HuggingFace API request failed: {str(e)}")

    def _chat_local(
        self,
        model_id: str,
        messages: Union[str, List[Dict[str, str]]],
        temperature: float,
        max_tokens: int,
        top_p: float,
        top_k: int,
        **kwargs,
    ) -> Dict[str, Any]:
        """Generate response using locally loaded model"""
        model, tokenizer = self._load_model_locally(model_id)

        # Format messages
        if isinstance(messages, str):
            prompt = messages
        else:
            prompt = self._format_messages(messages)

        # Tokenize input
        inputs = tokenizer(prompt, return_tensors="pt").to(self.device)

        # Generate response
        with torch.no_grad():
            outputs = model.generate(
                **inputs,
                max_new_tokens=max_tokens,
                temperature=temperature,
                top_p=top_p,
                top_k=top_k,
                do_sample=True,
                pad_token_id=tokenizer.eos_token_id,
                **kwargs,
            )

        # Decode response
        generated_text = tokenizer.decode(outputs[0], skip_special_tokens=True)

        # Remove prompt from response
        if prompt in generated_text:
            response_text = generated_text[len(prompt) :].strip()
        else:
            response_text = generated_text.strip()

        return {
            "response": response_text,
            "model": model_id,
            "provider": "huggingface",
            "method": "local",
        }

    def _format_messages(self, messages: List[Dict[str, str]]) -> str:
        """
        Format message list into a prompt string
        Handles different chat template formats
        """
        if not messages:
            return ""

        # Try to use tokenizer's chat template if available
        # Otherwise, use simple formatting
        formatted = ""
        for msg in messages:
            role = msg.get("role", "user")
            content = msg.get("content", "")
            if role == "system":
                formatted += f"System: {content}\n\n"
            elif role == "user":
                formatted += f"User: {content}\n\n"
            elif role == "assistant":
                formatted += f"Assistant: {content}\n\n"

        formatted += "Assistant: "
        return formatted

    def stream_chat(
        self,
        model_id: str,
        messages: Union[str, List[Dict[str, str]]],
        temperature: float = DEFAULT_TEMPERATURE,
        max_tokens: int = DEFAULT_MAX_TOKENS,
        **kwargs,
    ):
        """
        Stream chat responses (yields tokens as they're generated)
        Note: Streaming is primarily supported for local models
        """
        if not self.use_local:
            # For API, we can't easily stream, so return full response
            result = self.chat(model_id, messages, temperature, max_tokens, **kwargs)
            yield result["response"]
            return

        model, tokenizer = self._load_model_locally(model_id)

        if isinstance(messages, str):
            prompt = messages
        else:
            prompt = self._format_messages(messages)

        inputs = tokenizer(prompt, return_tensors="pt").to(self.device)

        with torch.no_grad():
            for output in model.generate(
                **inputs,
                max_new_tokens=max_tokens,
                temperature=temperature,
                do_sample=True,
                pad_token_id=tokenizer.eos_token_id,
                **kwargs,
            ):
                generated_text = tokenizer.decode(output, skip_special_tokens=True)
                if prompt in generated_text:
                    response_text = generated_text[len(prompt) :].strip()
                else:
                    response_text = generated_text.strip()
                yield response_text

    def list_available_models(self) -> List[str]:
        """List available models (returns configured models)"""
        from .config import HUGGINGFACE_CHATBOT_MODELS
        return list(HUGGINGFACE_CHATBOT_MODELS.keys())

