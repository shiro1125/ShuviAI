"""
Configuration loader for ShuviAI.

This module reads environment variables from a `.env` file using
`python‑dotenv` and exposes them as module‑level constants. Keeping
configuration in one place makes it easy to manage secrets and feature
toggles without hard‑coding them in the codebase.
"""

import os
from dotenv import load_dotenv


# Load variables from .env into the process environment. If the .env file
# does not exist, this call silently does nothing.
load_dotenv()


def _str_to_bool(value: str | None, default: bool = False) -> bool:
    """
    Convert a string to a boolean. Useful for parsing environment variables.

    Parameters
    ----------
    value : str | None
        The string to convert. If `None`, the default is returned.
    default : bool, optional
        The value to return if `value` is `None` or cannot be parsed.

    Returns
    -------
    bool
        The parsed boolean.
    """
    if value is None:
        return default
    return value.strip().lower() in {"1", "true", "yes", "y"}


# API key for the Gemini model. Set this in your .env file.
GEMINI_API_KEY: str | None = os.getenv("GEMINI_API_KEY")

# Toggle for text‑to‑speech. When True, the program will speak AI responses.
USE_TTS: bool = _str_to_bool(os.getenv("USE_TTS"), default=False)


__all__ = [
    "GEMINI_API_KEY",
    "USE_TTS",
]