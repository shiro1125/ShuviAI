"""
Configuration loader for ShuviAI.

This module reads environment variables from a `.env` file using
`python‑dotenv` and exposes them as module‑level constants. Keeping
configuration in one place makes it easy to manage secrets and feature
toggles without hard‑coding them in the codebase.
"""

import os
from dotenv import load_dotenv, find_dotenv


# Load variables from a .env file into the process environment.  Using
# find_dotenv() ensures that the .env file is located starting from the
# project root when the program is executed from different working
# directories.  If the .env file does not exist, this call silently does
# nothing.
_dotenv_path = find_dotenv()
load_dotenv(dotenv_path=_dotenv_path)


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


# API key for the Gemini model. Set this in your .env file.  Without this
# key the AI integration will not work.
GEMINI_API_KEY: str | None = os.getenv("GEMINI_API_KEY")

# Optional: specify a Gemini model name.  Defaults to models/gemini-pro if
# unspecified.
GEMINI_MODEL: str | None = os.getenv("GEMINI_MODEL")

# Toggle for text‑to‑speech. When True, the program will speak AI responses.
USE_TTS: bool = _str_to_bool(os.getenv("USE_TTS"), default=False)


__all__ = [
    "GEMINI_API_KEY",
    "GEMINI_MODEL",
    "USE_TTS",
]