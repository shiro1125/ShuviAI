"""
Audio input handling for ShuviAI.

This module encapsulates microphone access and speech recognition. It uses
the `speech_recognition` library to record from the default system
microphone and transcribe spoken Korean into text using Google's speech
recognition service. If you need offline transcription or another
language, you can modify the `listen_and_transcribe` function accordingly.
"""

from __future__ import annotations

import threading
from typing import Optional

import speech_recognition as sr


def _prompt_manual_input() -> str:
    """Prompt the user to type text input as a fallback."""
    try:
        return input("[MANUAL INPUT] Please type your query and press Enter: ").strip()
    except Exception:
        # If input fails (e.g. non-interactive environment), return empty string
        return ""


def listen_and_transcribe(language: str = "ko-KR") -> Optional[str]:
    """
    Listen to the microphone and convert speech to text.  If microphone access
    fails (e.g. PyAudio is missing or no microphone is connected), prompt the
    user to type input manually.

    Parameters
    ----------
    language : str, optional
        The language code for recognition (default is Korean: 'ko-KR'). See the
        SpeechRecognition documentation for supported languages.

    Returns
    -------
    Optional[str]
        The recognized text, or the typed string if microphone input is not
        available.  Returns ``None`` only if recognition fails.
    """
    recognizer = sr.Recognizer()
    try:
        # Attempt to access the default microphone.  This will fail if
        # the PyAudio library is not installed or no microphone is available.
        with sr.Microphone() as source:
            # Reduce ambient noise impact by calibrating for a short period.
            recognizer.adjust_for_ambient_noise(source, duration=0.5)
            print("[INFO] Listening... Please speak now.")
            audio_data = recognizer.listen(source)

        # Attempt to recognize speech using Google's speech recognition API.
        try:
            text = recognizer.recognize_google(audio_data, language=language)
            return text
        except sr.UnknownValueError:
            # Audio was heard but could not be understood.
            print("[INFO] Speech was not understood. Please try again.")
            return None
        except sr.RequestError as e:
            # Network or API error.
            print(f"[ERROR] Speech recognition service error: {e}")
            return None

    except AttributeError as attr_err:
        # PyAudio is likely missing if attribute errors are raised when
        # initializing the microphone.
        print(
            "[ERROR] PyAudio library not found. Microphone input requires the PyAudio library.\n"
            "Install PyAudio on Windows by running:\n"
            "    pip install pipwin\n"
            "    pipwin install pyaudio\n"
            "Alternatively, ensure that PyAudio is properly installed for your platform."
        )
        # Fall back to manual text input so the program remains usable.
        return _prompt_manual_input() or None

    except OSError as os_err:
        # OSError indicates no default input device or other system‑level issues.
        print(f"[ERROR] Microphone error: {os_err}")
        print(
            "No microphone was detected or it is currently unavailable. Please connect a microphone "
            "and try again, or type your input below."
        )
        return _prompt_manual_input() or None

    except Exception as exc:
        # Catch any other errors accessing the microphone or the recognizer.
        print(f"[ERROR] Unexpected audio input error: {exc}")
        return None