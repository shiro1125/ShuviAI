"""
Gemini integration for ShuviAI.

This module provides a simple wrapper around Google's Gemini API using the
`google-generativeai` SDK.  The primary entry point is `generate_reply`,
which accepts a prompt string and returns the model's response as text.

Environment variables:
    GEMINI_API_KEY: The API key used to authenticate with Google AI services.
    GEMINI_MODEL: Optional model name. Defaults to "models/gemini-pro".

The model name can be changed by setting GEMINI_MODEL in your `.env` file.
Consult Google AI Studio for the list of available models.
"""

from __future__ import annotations

from typing import Optional

import google.generativeai as genai  # type: ignore

import config

# Determine which model to use.  If unspecified, default to models/gemini-pro.
_DEFAULT_MODEL: str = config.GEMINI_MODEL or "gemini-3.1-flash-lite-preview"


def _configure_client() -> None:
    """Configure the generative AI client with the API key.

    This function must be called before any model is instantiated.  It
    configures the underlying SDK with the API key defined in the
    environment.  If the API key is missing or invalid, a RuntimeError is
    raised.
    """
    try:
        # The generative AI SDK uses a global configuration.  Calling
        # configure() repeatedly is inexpensive; however, we guard against
        # missing API keys here.
        genai.configure(api_key=config.GEMINI_API_KEY)
    except Exception as exc:
        raise RuntimeError(
            "Failed to configure Google Generative AI client. Please check your API key."
        ) from exc


def generate_reply(prompt: str) -> Optional[str]:
    """
    Generate a reply from the Gemini model given an input prompt.

    Parameters
    ----------
    prompt : str
        The user input or conversation history to provide to the model.

    Returns
    -------
    Optional[str]
        The model's textual response, or ``None`` if the request fails.
    """
    # Ensure the client is configured with the API key.
    try:
        _configure_client()
    except RuntimeError as err:
        print(f"[ERROR] {err}")
        return None

    # Instantiate a generative model.  Using models/* path is required for
    # compatibility with the Gemini API.  For example: 'models/gemini-pro'.
    model_name: str = _DEFAULT_MODEL
    try:
        model = genai.GenerativeModel(model_name)
    except Exception as exc:
        print(f"[ERROR] Failed to load Gemini model '{model_name}': {exc}")
        return None

    # Generate content from the model.  The SDK returns a response object whose
    # `text` attribute holds the generated text.  Use getattr to avoid
    # AttributeError when the response does not contain text (e.g. image output).
    try:
        response = model.generate_content(prompt)
        return getattr(response, "text", None)
    except Exception as exc:
        print(f"[ERROR] Gemini API call failed: {exc}")
        return None


__all__ = ["generate_reply"]