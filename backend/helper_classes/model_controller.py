import os
from enum import Enum
from dotenv import load_dotenv
import openai
from google import generativeai as genai

load_dotenv()

class ModelProvider(Enum):
    GEMINI = "gemini"
    OPENAI = "openai"
    OLLAMA = "ollama"

def get_env_var(name: str) -> str:
    value = os.getenv(name)
    if not value:
        raise EnvironmentError(f"Umgebungsvariable '{name}' ist nicht gesetzt.")
    return value

class ModelController:
    def __init__(self, provider: ModelProvider):
        self.provider = provider

        # Models
        self.gemini_model = get_env_var("GEMINI_MODEL")
        self.openai_model = get_env_var("OPENAI_MODEL")
        self.ollama_model = get_env_var("OLLAMA_MODEL")
        self.ollama_api_url = get_env_var("OLLAMA_API_URL")

        # API-Key-Lists
        self.api_keys = {
            ModelProvider.GEMINI: self._load_keys("GEMINI_API_KEYS"),
            ModelProvider.OPENAI: self._load_keys("OPENAI_API_KEYS"),
            ModelProvider.OLLAMA: self._load_keys("OLLAMA_API_KEYS")
        }

        # Current api list indexes
        self.api_key_index = {
            ModelProvider.GEMINI: 0,
            ModelProvider.OPENAI: 0,
            ModelProvider.OLLAMA: 0
        }

        self._init_provider(provider)

    def _load_keys(self, env_name: str):
        raw = get_env_var(env_name)
        keys = [k.strip() for k in raw.split(",") if k.strip()]
        if not keys:
            raise ValueError(f"No API key found for {env_name}.")
        return keys

    def _get_current_key(self, provider: ModelProvider):
        return self.api_keys[provider][self.api_key_index[provider]]

    def _next_api_key(self, provider: ModelProvider):
        self.api_key_index[provider] += 1
        if self.api_key_index[provider] >= len(self.api_keys[provider]):
            raise RuntimeError(f"All API keys for {provider.value} are used up.")
        return self._get_current_key(provider)

    def _init_provider(self, provider: ModelProvider):
        key = self._get_current_key(provider)
        if provider == ModelProvider.GEMINI:
            genai.configure(api_key=key)
            self.gemini_client = genai.GenerativeModel(model_name=self.gemini_model)
        elif provider == ModelProvider.OPENAI:
            openai.api_key = key
        elif provider == ModelProvider.OLLAMA:
            # will be defined in header later
            pass
        else:
            raise ValueError(f"Unknown provider: {provider}")

    def switch_provider(self, provider: ModelProvider):
        self.provider = provider
        self._init_provider(provider)

    def generate_text(self, prompt: str) -> str:
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
                    print(f"Ollama-Fehler: {e} – Wechsle Key...")
                    self._next_api_key(ModelProvider.OLLAMA)
                except Exception as e:
                    raise RuntimeError(f"Ollama-Fehler: {e}")

        else:
            raise ValueError(f"Unsupported provider: {self.provider}")


#controller = ModelController(provider=ModelProvider.GEMINI)
#print("Gemini:", controller.generate_text("Was ist künstliche Intelligenz? keep it short"))

#controller = ModelController(provider=ModelProvider.OLLAMA)
#print("Ollama:", controller.generate_text("Was ist künstliche Intelligenz? keep it short"))

#controller = ModelController(provider=ModelProvider.OPENAI)
#print("OpenAi:", controller.generate_text("Was ist künstliche Intelligenz? keep it short"))
