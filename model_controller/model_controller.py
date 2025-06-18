import os
from enum import Enum
from dotenv import load_dotenv
import openai
from google import generativeai as genai


# Lade Umgebungsvariablen
load_dotenv()


class ModelProvider(Enum):
    GEMINI = "gemini"
    OPENAI = "openai"


def get_env_var(name: str) -> str:
    value = os.getenv(name)
    if not value:
        raise EnvironmentError(f"Umgebungsvariable '{name}' ist nicht gesetzt.")
    return value


class ModelController:
    def __init__(self, provider: ModelProvider):
        self.provider = provider

        # Erforderliche Variablen laden (Fehler bei Fehlen)
        self.gemini_api_key = get_env_var("GEMINI_API_KEY")
        self.gemini_model = get_env_var("GEMINI_MODEL")
        self.openai_api_key = get_env_var("OPENAI_API_KEY")
        self.openai_model = get_env_var("OPENAI_MODEL")

        # Initialisiere gewählten Provider
        self._init_provider(provider)

    def _init_provider(self, provider: ModelProvider):
        if provider == ModelProvider.GEMINI:
            genai.configure(api_key=self.gemini_api_key)
            self.gemini_client = genai.GenerativeModel(model_name=self.gemini_model)
        elif provider == ModelProvider.OPENAI:
            openai.api_key = self.openai_api_key
        else:
            raise ValueError(f"Unbekannter Provider: {provider}")

    def switch_provider(self, provider: ModelProvider):
        self.provider = provider
        self._init_provider(provider)

    def generate_text(self, prompt: str) -> str:
        if self.provider == ModelProvider.GEMINI:
            response = self.gemini_client.generate_content(prompt)
            return response.text.strip()
        elif self.provider == ModelProvider.OPENAI:
            response = openai.ChatCompletion.create(
                model=self.openai_model,
                messages=[{"role": "user", "content": prompt}]
            )
            return response["choices"][0]["message"]["content"].strip()
        else:
            raise ValueError(f"Unsupported provider: {self.provider}")

controller = ModelController(provider=ModelProvider.GEMINI)
print("Gemini:", controller.generate_text("Was ist künstliche Intelligenz?"))