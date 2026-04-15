"""
Audio input handling for ShuviAI.

This module encapsulates microphone access and speech recognition. It uses
the `speech_recognition` library to record from the default system
microphone and transcribe spoken Korean into text using Google's speech
recognition service. If you need offline transcription or another
language, you can modify the `listen_and_transcribe` function accordingly.
"""

from __future__ import annotations

import speech_recognition as sr
from typing import Optional


def listen_and_transcribe(language: str = "ko-KR") -> Optional[str]:
    """
    Listen to the microphone and convert speech to text.

    Parameters
    ----------
    language : str, optional
        The language code for recognition (default is Korean: 'ko-KR'). See the
        SpeechRecognition documentation for supported languages.

    Returns
    -------
    Optional[str]
        The recognized text, or ``None`` if recognition failed.
    """
    recognizer = sr.Recognizer()
    try:
        # Use the default microphone as the audio source
        with sr.Microphone() as source:
            # Adjust the recognizer sensitivity to ambient noise and record audio
            recognizer.adjust_for_ambient_noise(source, duration=0.5)
            print("[INFO] Listening...")
            audio_data = recognizer.listen(source)

        # Attempt to recognize speech using Google's free API
        try:
            text = recognizer.recognize_google(audio_data, language=language)
            return text
        except sr.UnknownValueError:
            # Audio was heard but could not be understood
            return None
        except sr.RequestError as e:
            print(f"[ERROR] Speech recognition service error: {e}")
            return None

    except Exception as exc:
        # Catch any errors accessing the microphone or the recognizer
        print(f"[ERROR] Microphone error: {exc}")
        return None