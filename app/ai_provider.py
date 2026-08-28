from __future__ import annotations

from dataclasses import dataclass
import os


class AIProviderError(ValueError):
    """Raised when an AI provider is not configured or supported."""


@dataclass(frozen=True)
class AIProviderConfig:
    name: str
    api_key: str
    base_url: str
    model: str

    @property
    def chat_completions_url(self) -> str:
        base = self.base_url.rstrip("/")
        if base.endswith("/openai"):
            return f"{base}/chat/completions"
        return f"{base}/v1/chat/completions"

    @property
    def responses_url(self) -> str:
        base = self.base_url.rstrip("/")
        return f"{base}/v1/responses"

    @property
    def uses_responses_api(self) -> bool:
        return self.name in {"openai", "chatgpt"}


def resolve_ai_provider() -> AIProviderConfig:
    name = os.getenv("AI_PROVIDER", "terra").strip().lower()
    settings = {
        "terra": ("TERRA_API_KEY", "TERRA_API_BASE_URL", "TERRA_MODEL", "gpt-5.6-terra"),
        "openai": ("OPENAI_API_KEY", "OPENAI_API_BASE_URL", "OPENAI_MODEL", "gpt-5"),
        "chatgpt": ("OPENAI_API_KEY", "OPENAI_API_BASE_URL", "OPENAI_MODEL", "gpt-5"),
        "gemini": ("GEMINI_API_KEY", "GEMINI_API_BASE_URL", "GEMINI_MODEL", "gemini-2.5-flash"),
    }
    if name not in settings:
        raise AIProviderError("AI_PROVIDER must be terra, openai, chatgpt, or gemini.")
    key_name, base_name, model_name, default_model = settings[name]
    api_key = os.getenv(key_name, "")
    base_url = os.getenv(base_name, "")
    model = os.getenv(model_name, default_model)
    if not api_key.strip() or not base_url.startswith(("http://", "https://")):
        raise AIProviderError(f"{name} AI provider is not fully configured.")
    return AIProviderConfig(name, api_key, base_url, model)


def chat_completions_url(base_url: str) -> str:
    base = base_url.rstrip("/")
    return f"{base}/chat/completions" if base.endswith("/openai") else f"{base}/v1/chat/completions"


def responses_url(base_url: str) -> str:
    return f"{base_url.rstrip('/')}/v1/responses"
