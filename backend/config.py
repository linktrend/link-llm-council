"""Configuration for the LLM Council."""

import os
from dotenv import load_dotenv

load_dotenv()

# OpenRouter API key
OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")

_DEFAULT_COUNCIL_MODELS = [
    "openai/gpt-5.1",
    "google/gemini-3.1-pro-preview",
    "anthropic/claude-sonnet-4.5",
    "google/gemini-3-flash-preview",
]

_DEFAULT_CHAIRMAN_MODEL = "google/gemini-3.1-pro-preview"

_DEFAULT_CHAIRMAN_FALLBACK_MODELS = [
    "anthropic/claude-sonnet-4.5",
    "openai/gpt-5.1",
]


def _parse_model_list(raw: str | None, default: list[str]) -> list[str]:
    """Parse comma-separated OpenRouter model ids from env."""
    if not raw:
        return default
    models = [item.strip() for item in raw.split(",") if item.strip()]
    return models or default


# Council members - list of OpenRouter model identifiers
COUNCIL_MODELS = _parse_model_list(os.getenv("COUNCIL_MODELS"), _DEFAULT_COUNCIL_MODELS)

# Chairman model - synthesizes final response
CHAIRMAN_MODEL = os.getenv("CHAIRMAN_MODEL", _DEFAULT_CHAIRMAN_MODEL).strip() or _DEFAULT_CHAIRMAN_MODEL

# Fallback chairman models when the primary chairman fails (404, timeout, etc.)
CHAIRMAN_FALLBACK_MODELS = _parse_model_list(
    os.getenv("CHAIRMAN_FALLBACK_MODELS"),
    _DEFAULT_CHAIRMAN_FALLBACK_MODELS,
)

# OpenRouter API endpoint
OPENROUTER_API_URL = "https://openrouter.ai/api/v1/chat/completions"

# Data directory for conversation storage
DATA_DIR = "data/conversations"
