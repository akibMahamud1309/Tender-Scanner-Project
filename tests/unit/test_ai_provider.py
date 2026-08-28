import pytest

from app.ai_provider import AIProviderError, chat_completions_url, resolve_ai_provider


def test_resolve_ai_provider_supports_openai(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv("AI_PROVIDER", "chatgpt")
    monkeypatch.setenv("OPENAI_API_KEY", "key")
    monkeypatch.setenv("OPENAI_API_BASE_URL", "https://api.openai.com")
    config = resolve_ai_provider()
    assert config.name == "chatgpt"
    assert config.model == "gpt-5"
    assert config.chat_completions_url.endswith("/v1/chat/completions")


def test_resolve_ai_provider_supports_gemini_openai_compatibility(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv("AI_PROVIDER", "gemini")
    monkeypatch.setenv("GEMINI_API_KEY", "key")
    monkeypatch.setenv("GEMINI_API_BASE_URL", "https://generativelanguage.googleapis.com/v1beta/openai")
    assert resolve_ai_provider().chat_completions_url.endswith("/openai/chat/completions")


def test_resolve_ai_provider_rejects_unknown_provider(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv("AI_PROVIDER", "unknown")
    with pytest.raises(AIProviderError):
        resolve_ai_provider()


def test_chat_completions_url_preserves_explicit_openai_compatible_path() -> None:
    assert chat_completions_url("https://provider.example/openai") == "https://provider.example/openai/chat/completions"
