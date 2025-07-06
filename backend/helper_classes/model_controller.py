"""
This module provides a controller for managing interactions with various Large Language Models (LLMs).

It defines a `ModelController` class that can switch between different LLM providers like Gemini, OpenAI, and Ollama.
The controller handles API key management, including loading keys from environment variables and rotating them 
if an API call fails. This allows for a resilient and flexible way to generate text using different models.

Key Features:
- Support for multiple LLM providers (Gemini, OpenAI, Ollama).
- Automatic loading of API keys and model configurations from environment variables.
- API key rotation to handle authentication errors or other API issues.
- A unified `generate_text` method to interact with any of the supported models.

.env File Specifications:
The script requires a .env file in the root directory with the following variables:

# Model names
GEMINI_MODEL="gemini-pro"
OPENAI_MODEL="gpt-4"
OLLAMA_MODEL="llama2"

# API URL for Ollama
OLLAMA_API_URL="http://localhost:11434"

# Comma-separated API keys
GEMINI_API_KEYS="your_gemini_api_key_1,your_gemini_api_key_2"
OPENAI_API_KEYS="your_openai_api_key_1,your_openai_api_key_2"
OLLAMA_API_KEYS="your_ollama_api_key_1,your_ollama_api_key_2"
"""
import os
from enum import Enum
from dotenv import load_dotenv
import openai
from google import generativeai as genai

load_dotenv()

class ModelProvider(Enum):
    """Enumeration for the supported LLM providers."""
    GEMINI = "gemini"
    OPENAI = "openai"
    OLLAMA = "ollama"

def get_env_var(name: str) -> str:
    """
    Retrieves an environment variable and raises an error if it's not set.

    Args:
        name (str): The name of the environment variable.

    Raises:
        EnvironmentError: If the environment variable is not set.

    Returns:
        str: The value of the environment variable.
    """
    value = os.getenv(name)
    if not value:
        raise EnvironmentError(f"Environment variable '{name}' is not set.")
    return value

class ModelController:
    """Manages text generation using various LLM providers."""
    def __init__(self, provider: ModelProvider):
        """
        Initializes the ModelController for a specific provider.

        Args:
            provider (ModelProvider): The LLM provider to use (e.g., ModelProvider.GEMINI).
        """
        self.provider = provider

        # Load model configurations from environment variables
        self.gemini_model = get_env_var("GEMINI_MODEL")
        self.openai_model = get_env_var("OPENAI_MODEL")
        self.ollama_model = get_env_var("OLLAMA_MODEL")
        self.ollama_api_url = get_env_var("OLLAMA_API_URL")

        # Load API keys for each provider
        self.api_keys = {
            ModelProvider.GEMINI: self._load_keys("GEMINI_API_KEYS"),
            ModelProvider.OPENAI: self._load_keys("OPENAI_API_KEYS"),
            ModelProvider.OLLAMA: self._load_keys("OLLAMA_API_KEYS")
        }

        # Track the current API key index for each provider
        self.api_key_index = {
            ModelProvider.GEMINI: 0,
            ModelProvider.OPENAI: 0,
            ModelProvider.OLLAMA: 0
        }

        self._init_provider(provider)

    def _load_keys(self, env_name: str):
        """
        Loads a comma-separated list of API keys from an environment variable.

        Args:
            env_name (str): The name of the environment variable containing the API keys.

        Raises:
            ValueError: If no API keys are found in the environment variable.

        Returns:
            list: A list of API keys.
        """
        raw = get_env_var(env_name)
        keys = [k.strip() for k in raw.split(",") if k.strip()]
        if not keys:
            raise ValueError(f"No API key found for {env_name}.")
        return keys

    def _get_current_key(self, provider: ModelProvider):
        """Gets the current API key for the specified provider."""
        return self.api_keys[provider][self.api_key_index[provider]]

    def _next_api_key(self, provider: ModelProvider):
        """
        Moves to the next available API key for the provider.

        Raises:
            RuntimeError: If all API keys for the provider have been used.

        Returns:
            str: The next API key.
        """
        self.api_key_index[provider] += 1
        if self.api_key_index[provider] >= len(self.api_keys[provider]):
            raise RuntimeError(f"All API keys for {provider.value} are used up.")
        return self._get_current_key(provider)

    def _init_provider(self, provider: ModelProvider):
        """
        Initializes the client for the specified provider with the current API key.

        Args:
            provider (ModelProvider): The provider to initialize.

        Raises:
            ValueError: If the provider is unknown.
        """
        key = self._get_current_key(provider)
        if provider == ModelProvider.GEMINI:
            genai.configure(api_key=key)
            self.gemini_client = genai.GenerativeModel(model_name=self.gemini_model)
        elif provider == ModelProvider.OPENAI:
            openai.api_key = key
        elif provider == ModelProvider.OLLAMA:
            # For Ollama, the key is sent in the request header, so no client-side initialization is needed here.
            pass
        else:
            raise ValueError(f"Unknown provider: {provider}")

    def switch_provider(self, provider: ModelProvider):
        """Switches to a different LLM provider and initializes it."""
        self.provider = provider
        self._init_provider(provider)

    def generate_text(self, prompt: str) -> str:
        """
        Generates text using the currently configured LLM provider.

        This method will automatically try the next available API key if an error occurs during generation.

        Args:
            prompt (str): The input prompt for the LLM.

        Raises:
            RuntimeError: If an unrecoverable error occurs with the API.
            ValueError: If the configured provider is unsupported.

        Returns:
            str: The generated text, stripped of leading/trailing whitespace.
        """
        if self.provider == ModelProvider.GEMINI:
            while True:
                try:
                    response = self.gemini_client.generate_content(prompt)
                    return response.text.strip()
                except Exception as e:
                    print(f"Gemini-Error: {e} – Changing key...")
                    self._next_api_key(ModelProvider.GEMINI)
                    self._init_provider(ModelProvider.GEMINI)

        elif self.provider == ModelProvider.OPENAI:
            while True:
                try:
                    response = openai.ChatCompletion.create(
                        model=self.openai_model,
                        messages=[{"role": "user", "content": prompt}]
                    )
                    return response["choices"][0]["message"]["content"].strip()
                except openai.error.AuthenticationError:
                    print("OpenAI-Auth-Error – Changing Key...")
                    self._next_api_key(ModelProvider.OPENAI)
                    self._init_provider(ModelProvider.OPENAI)
                except Exception as e:
                    raise RuntimeError(f"OpenAI-Error: {e}")

        elif self.provider == ModelProvider.OLLAMA:
            import requests
            while True:
                try:
                    headers = {
                        "Authorization": f"Bearer {self._get_current_key(ModelProvider.OLLAMA)}",
                        "Content-Type": "application/json"
                    }
                    data = {
                        "model": self.ollama_model,
                        "prompt": prompt,
                        "stream": False
                    }
                    response = requests.post(f"{self.ollama_api_url}/api/generate", json=data, headers=headers)
                    response.raise_for_status()
                    return response.json()["response"].strip()
                except requests.exceptions.HTTPError as e:
                    print(f"Ollama-Error: {e} – Changing key...")
                    self._next_api_key(ModelProvider.OLLAMA)
                except Exception as e:
                    raise RuntimeError(f"Ollama-Error: {e}")

        else:
            raise ValueError(f"Unsupported provider: {self.provider}")


# Example usage (commented out):
# controller = ModelController(provider=ModelProvider.GEMINI)
# print("Gemini:", controller.generate_text("What is artificial intelligence? Keep it short."))
#
# controller = ModelController(provider=ModelProvider.OLLAMA)
# print("Ollama:", controller.generate_text("What is artificial intelligence? Keep it short."))
#
# controller = ModelController(provider=ModelProvider.OPENAI)
# print("OpenAI:", controller.generate_text("What is artificial intelligence? Keep it short."))
