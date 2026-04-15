"""
Gemini integration for ShuviAI.

This module abstracts calls to Google's Gemini API using the
`google‑generativeai` SDK. The primary entry point is `generate_reply`,
which accepts a prompt string and returns the model's response as text.

Environment variables:
    GEMINI_API_KEY: The API key used to authenticate with Google AI services.
    GEMINI_MODEL: Optional model name. Defaults to "models/gemini-pro".

The model name can be changed by setting GEMINI_MODEL in your `.env` file.
Consult Google AI Studio for the list of available models.
"""

from __future__ import annotations

import os
from typing import Optional

from google import genai  # type: ignore
import config


# Determine which model to use. If unspecified, default to gemini‑pro.
_DEFAULT_MODEL = os.getenv("GEMINI_MODEL", "models/gemini-pro")


def _get_client() -> genai.Client:
    """Initialize and return a genai.Client using the configured API key."""
    return genai.Client(
        api_key=config.GEMINI_API_KEY,
        http_options={"api_version": "v1beta"},
    )


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
    client = _get_client()
    try:
        # For most models, we can call generate_content with the prompt string
        # directly. If your selected model requires a different API, you can
        # modify this call accordingly.
        response = client.models.generate_content(
            model=_DEFAULT_MODEL,
            contents=prompt,
        )
        # The response object exposes the generated text via a `text` attribute.
        return getattr(response, "text", None)
    except Exception as exc:
        print(f"[ERROR] Gemini API call failed: {exc}")
        return None