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

import config
from input.voice_input import listen_and_transcribe
from ai.gemini import generate_reply

try:
    # Attempt to import the TTS module conditionally. This allows running the
    # application without TTS dependencies if USE_TTS is False.
    if config.USE_TTS:
        from tts.speech import speak
    else:
        speak = None  # type: ignore
except Exception:
    # If TTS import fails, fall back to None and warn the user.
    speak = None  # type: ignore


def main() -> None:
    """Main loop that orchestrates voice input, AI processing and output."""
    if not config.GEMINI_API_KEY:
        print(
            "[ERROR] GEMINI_API_KEY is not set. Please copy .env.example to .env and "
            "provide your API key."
        )
        sys.exit(1)

    print("ShuviAI is running. Speak into your microphone to begin.")
    print("Press Ctrl+C to exit.")

    while True:
        try:
            # Record audio and convert to text
            user_text = listen_and_transcribe()
            if not user_text:
                print("[INFO] Could not understand audio. Please try again.")
                continue

            print(f"[USER] {user_text}")

            # Generate a reply using the Gemini model
            ai_response = generate_reply(user_text)
            if ai_response:
                print(f"[AI] {ai_response}")
                # Optionally speak the response aloud
                if config.USE_TTS and speak:
                    try:
                        speak(ai_response)
                    except Exception:
                        # Catch any TTS errors to prevent the program from crashing
                        print("[WARNING] Failed to speak response. See traceback for details.")
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