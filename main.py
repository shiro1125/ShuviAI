"""
Entry point for ShuviAI.

This script ties together the input, AI and TTS modules. It listens for speech
from the user's microphone, transcribes it to text, sends the text to the
Gemini model to generate a response, and prints the result. If text‑to‑speech
is enabled via the `USE_TTS` configuration flag, the response will also be
spoken aloud.

Run this file directly to start the application.
"""

import sys
import traceback
from typing import Optional, Callable, Any

from concurrent.futures import ThreadPoolExecutor, TimeoutError

import config
from ai.gemini import generate_reply
from input.voice_input import listen_and_transcribe

try:
    # Attempt to import the TTS module conditionally. This allows running the
    # application without TTS dependencies if USE_TTS is False.
    if config.USE_TTS:
        from tts.speech import speak  # type: ignore
    else:
        speak = None  # type: ignore
except Exception:
    # If TTS import fails, fall back to None and warn the user.
    speak = None  # type: ignore


def _call_with_timeout(func: Callable[..., Any], *args: Any, timeout: float = 60.0) -> Optional[str]:
    """
    Call the provided function in a separate thread and return its result,
    enforcing a timeout.  If the function does not complete within
    `timeout` seconds, return ``None`` and log an error.  Any exceptions
    raised during execution are caught and logged, and ``None`` is
    returned.

    Parameters
    ----------
    func : Callable[..., Any]
        The function to call.
    *args : Any
        Positional arguments to pass to the function.
    timeout : float, optional
        Number of seconds to wait for the function to complete.  Defaults
        to 60 seconds.

    Returns
    -------
    Optional[str]
        The return value of the function if successful and within
        timeout, otherwise ``None``.
    """
    with ThreadPoolExecutor(max_workers=1) as executor:
        future = executor.submit(func, *args)
        try:
            return future.result(timeout=timeout)
        except TimeoutError:
            print(f"[ERROR] AI request timed out after {timeout} seconds.")
            return None
        except Exception as exc:
            print(f"[ERROR] AI call failed: {exc}")
            return None


def _print_banner() -> None:
    """Print a startup banner explaining how to use the application."""
    print("ShuviAI is running.")
    print("• Speak into your microphone when prompted to ask a question.")
    print(
        "• If your microphone is unavailable or PyAudio is not installed, you can type your input manually when prompted."
    )
    print("Press Ctrl+C to exit at any time.\n")


def main() -> None:
    """Main loop that orchestrates voice input, AI processing and output."""
    if not config.GEMINI_API_KEY:
        print(
            "[ERROR] GEMINI_API_KEY is not set. Please copy .env.example to .env and "
            "provide your API key."
        )
        sys.exit(1)

    _print_banner()

    while True:
        try:
            # Record audio or accept manual text input and convert to text.
            user_text: Optional[str] = listen_and_transcribe()
            if user_text is None or user_text.strip() == "":
                # Input was not understood or no text was provided.
                print("[INFO] No input detected. Please try again.")
                continue

            print(f"[USER] {user_text}")

            # Generate a reply using the Gemini model with a timeout to
            # prevent the program from hanging if the API call takes too long.
            ai_response: Optional[str] = _call_with_timeout(generate_reply, user_text, timeout=60)
            if ai_response:
                print(f"[AI] {ai_response}")
                # Optionally speak the response aloud
                if config.USE_TTS and speak:
                    try:
                        speak(ai_response)
                    except Exception:
                        # Catch any TTS errors to prevent the program from crashing
                        print(
                            "[WARNING] Failed to speak response. The response will be displayed in text only."
                        )
                        traceback.print_exc()
            else:
                print("[INFO] No response from AI model.")

        except KeyboardInterrupt:
            print("\nExiting ShuviAI. Goodbye!")
            break
        except Exception:
            print("[ERROR] An unexpected error occurred while processing your request.")
            traceback.print_exc()


if __name__ == "__main__":
    main()