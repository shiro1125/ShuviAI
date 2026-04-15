"""
Text‑to‑speech (TTS) functionality for ShuviAI.

This module currently implements a simple offline TTS using the
`pyttsx3` library. When `speak` is called with a text string, the
function will synthesise and play the audio. If no suitable voice is
available for the target language, the default system voice will be used.

If you wish to integrate an external TTS provider (e.g. ElevenLabs), you
can extend this module accordingly and reference additional environment
variables (e.g. TTS_API_KEY, TTS_VOICE_ID). For now, the default offline
engine is sufficient for basic usage.
"""

from __future__ import annotations

import pyttsx3
from typing import Optional
import threading


_engine: Optional[pyttsx3.Engine] = None
_engine_lock = threading.Lock()


def _init_engine() -> pyttsx3.Engine:
    """Initialise the pyttsx3 engine lazily and return it."""
    global _engine
    with _engine_lock:
        if _engine is None:
            _engine = pyttsx3.init()
            # You may customise properties such as rate or volume here
            try:
                _engine.setProperty("rate", 180)
            except Exception:
                pass
        return _engine


def speak(text: str) -> None:
    """
    Speak the provided text aloud using the system's default TTS voice.

    Parameters
    ----------
    text : str
        The text to be spoken.
    """
    engine = _init_engine()
    try:
        engine.say(text)
        engine.runAndWait()
    except Exception as exc:
        print(f"[ERROR] TTS engine error: {exc}")