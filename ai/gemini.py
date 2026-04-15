"""
Gemini integration for ShuviAI using the Google Gen AI SDK.

This module provides a simple wrapper around Google's Gemini API using
the `google‑genai` package.  The primary entry point is
`generate_reply`, which accepts a prompt string and returns the
model's response as text.

Environment variables:
    GEMINI_API_KEY: The API key used to authenticate with Google AI services.
    GEMINI_MODEL: Optional model name. Defaults to "gemini-2.5-flash".

The model name can be changed by setting GEMINI_MODEL in your `.env`
file.  Consult the Gemini API documentation for the list of
available models and their capabilities.
"""

from __future__ import annotations

from typing import Optional

import google.genai as genai  # type: ignore

import config

# Determine which model to use.  If unspecified, default to gemini-2.5-flash.
_DEFAULT_MODEL: str = config.GEMINI_MODEL or "gemini-2.5-flash"


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
    # Ensure an API key is available.
    if not config.GEMINI_API_KEY:
        print(
            "[ERROR] GEMINI_API_KEY is not set. Please provide your API key in the .env file."
        )
        return None

    try:
        # Create a client for the Gemini Developer API.
        client = genai.Client(api_key=config.GEMINI_API_KEY)
    except Exception as exc:
        print(f"[ERROR] Failed to create Gemini client: {exc}")
        return None

    try:
        # Call the API to generate a reply.  The response object exposes
        # the generated text via its `text` attribute.
        response = client.models.generate_content(
            model=_DEFAULT_MODEL,
            contents=prompt,
        )
        return getattr(response, "text", None)
    except Exception as exc:
        print(f"[ERROR] Gemini API call failed: {exc}")
        return None
    finally:
        # Close the client to free network resources.
        try:
            client.close()
        except Exception:
            pass


__all__ = ["generate_reply"]