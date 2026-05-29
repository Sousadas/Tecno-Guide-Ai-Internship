"""
Day 13 — Voice AI Assistant
============================
A mini voice assistant that:
  1. Listens via the microphone (SpeechRecognition + PyAudio)
  2. Converts speech → text  (Google Web Speech API, free, no key required)
  3. Parses the text for known voice commands
  4. Responds with spoken output (pyttsx3 — offline TTS)

If PyAudio is not installed the assistant falls back to typed input so
you can still exercise the command-handling logic.

Dependencies
------------
pip install SpeechRecognition pyttsx3 pyaudio

Usage
-----
python voice_assistant.py            # mic mode  (needs pyaudio)
python voice_assistant.py --text     # text mode  (no mic needed)
"""

import argparse
import datetime
import os
import platform
import random
import subprocess
import sys
import webbrowser

# ---------------------------------------------------------------------------
# 1.  Speech Recognition setup
# ---------------------------------------------------------------------------
import speech_recognition as sr

# Try to import pyttsx3 for text-to-speech
try:
    import pyttsx3
    TTS_AVAILABLE = True
except Exception:
    TTS_AVAILABLE = False

# Check if PyAudio is available (needed for microphone input)
try:
    import pyaudio  # noqa: F401
    MIC_AVAILABLE = True
except ImportError:
    MIC_AVAILABLE = False


# ---------------------------------------------------------------------------
# 2.  Text-to-Speech (TTS) helper
# ---------------------------------------------------------------------------
class Speaker:
    """Wrapper around pyttsx3 for spoken output."""

    def __init__(self):
        if TTS_AVAILABLE:
            self.engine = pyttsx3.init()
            # Slightly slower rate for clarity
            self.engine.setProperty("rate", 175)
            voices = self.engine.getProperty("voices")
            # Try to pick a pleasant voice (index 1 is often female on macOS)
            if len(voices) > 1:
                self.engine.setProperty("voice", voices[1].id)
        else:
            self.engine = None

    def say(self, text: str):
        """Speak *text* aloud and also print it."""
        print(f"🤖  {text}")
        if self.engine:
            try:
                self.engine.say(text)
                self.engine.runAndWait()
            except Exception as exc:
                print(f"   (TTS error: {exc})")


# ---------------------------------------------------------------------------
# 3.  Speech Recognition helpers
# ---------------------------------------------------------------------------
def listen_from_mic(recognizer: sr.Recognizer, timeout: int = 5) -> str | None:
    """Record from the default microphone and return transcribed text."""
    with sr.Microphone() as source:
        print("\n🎤  Listening … (speak now)")
        recognizer.adjust_for_ambient_noise(source, duration=0.5)
        try:
            audio = recognizer.listen(source, timeout=timeout, phrase_time_limit=8)
        except sr.WaitTimeoutError:
            print("   ⏱  No speech detected (timeout).")
            return None

    print("   🔄  Recognizing …")
    try:
        text = recognizer.recognize_google(audio)
        print(f"   📝  You said: \"{text}\"")
        return text.lower()
    except sr.UnknownValueError:
        print("   ❌  Sorry, I couldn't understand that.")
        return None
    except sr.RequestError as exc:
        print(f"   ❌  Google API error: {exc}")
        return None


def listen_from_keyboard() -> str | None:
    """Fallback: read a command from stdin."""
    try:
        text = input("\n⌨️   Type a command (or 'quit'): ").strip()
        return text.lower() if text else None
    except (EOFError, KeyboardInterrupt):
        return "quit"


# ---------------------------------------------------------------------------
# 4.  Voice Command definitions
# ---------------------------------------------------------------------------
# Each command is a (keywords, handler_function) pair.  The dispatcher
# checks whether ALL keywords appear in the transcribed text.

def cmd_hello(speaker: Speaker, text: str):
    """Greet the user."""
    greetings = [
        "Hello! How can I help you today?",
        "Hey there! What can I do for you?",
        "Hi! Ready to assist you.",
    ]
    speaker.say(random.choice(greetings))


def cmd_time(speaker: Speaker, text: str):
    """Tell the current time."""
    now = datetime.datetime.now().strftime("%I:%M %p")
    speaker.say(f"The current time is {now}.")


def cmd_date(speaker: Speaker, text: str):
    """Tell today's date."""
    today = datetime.datetime.now().strftime("%A, %B %d, %Y")
    speaker.say(f"Today is {today}.")


def cmd_search(speaker: Speaker, text: str):
    """Open a Google search in the default browser."""
    # Strip known trigger words to get the query
    query = text
    for word in ("search", "for", "google", "look", "up"):
        query = query.replace(word, "")
    query = query.strip()
    if query:
        speaker.say(f"Searching the web for: {query}")
        webbrowser.open(f"https://www.google.com/search?q={query}")
    else:
        speaker.say("What would you like me to search for?")


def cmd_open_website(speaker: Speaker, text: str):
    """Open a website — e.g. 'open youtube'."""
    sites = {
        "youtube": "https://www.youtube.com",
        "google": "https://www.google.com",
        "github": "https://www.github.com",
        "wikipedia": "https://www.wikipedia.org",
        "reddit": "https://www.reddit.com",
        "stack overflow": "https://stackoverflow.com",
        "chatgpt": "https://chatgpt.com/",
    }
    for name, url in sites.items():
        if name in text:
            speaker.say(f"Opening {name}.")
            webbrowser.open(url)
            return
    speaker.say("I can open YouTube, Google, GitHub, Wikipedia, Reddit, or Stack Overflow.")


def cmd_system_info(speaker: Speaker, text: str):
    """Report basic system information."""
    info = (
        f"You are running {platform.system()} {platform.release()} "
        f"on a {platform.machine()} machine.  "
        f"Python version is {platform.python_version()}."
    )
    speaker.say(info)


def cmd_joke(speaker: Speaker, text: str):
    """Tell a programming joke."""
    jokes = [
        "Why do programmers prefer dark mode? Because light attracts bugs!",
        "There are only 10 types of people — those who understand binary and those who don't.",
        "A SQL query walks into a bar, sees two tables, and asks: Can I join you?",
        "Why was the JavaScript developer sad? Because he didn't Node how to Express himself.",
        "What's a programmer's favorite hangout? Foo Bar!",
    ]
    speaker.say(random.choice(jokes))


def cmd_calculate(speaker: Speaker, text: str):
    """Evaluate a simple math expression — e.g. 'calculate 12 plus 7'."""
    # Replace spoken operators with symbols
    expr = text
    for word in ("calculate", "what is", "what's", "compute", "solve"):
        expr = expr.replace(word, "")
    expr = (
        expr.replace("plus", "+")
        .replace("minus", "-")
        .replace("times", "*")
        .replace("multiplied by", "*")
        .replace("divided by", "/")
        .replace("over", "/")
        .replace("x", "*")
    )
    expr = expr.strip()
    if not expr:
        speaker.say("Please say an expression like: calculate 12 plus 7.")
        return
    try:
        # Safe evaluation — only allow digits and basic operators
        allowed = set("0123456789+-*/.(). ")
        if all(ch in allowed for ch in expr):
            result = eval(expr)  # safe because we filtered chars
            speaker.say(f"The answer is {result}.")
        else:
            speaker.say("Sorry, I can only do basic arithmetic.")
    except Exception:
        speaker.say(f"I couldn't evaluate: {expr}")


def cmd_help(speaker: Speaker, text: str):
    """List available voice commands."""
    help_text = (
        "Here are things I can do: "
        "Say hello. Tell the time or date. "
        "Search the web. Open a website like YouTube or GitHub. "
        "Tell a joke. Do basic math like 'calculate 5 plus 3'. "
        "Show system info. Or say quit to exit."
    )
    speaker.say(help_text)


# Command registry — (set_of_keywords, handler)
COMMANDS = [
    ({"hello"},                cmd_hello),
    ({"hi"},                   cmd_hello),
    ({"hey"},                  cmd_hello),
    ({"time"},                 cmd_time),
    ({"date"},                 cmd_date),
    ({"search"},               cmd_search),
    ({"look", "up"},           cmd_search),
    ({"open"},                 cmd_open_website),
    ({"system", "info"},       cmd_system_info),
    ({"joke"},                 cmd_joke),
    ({"calculate"},            cmd_calculate),
    ({"what", "is"},           cmd_calculate),
    ({"help"},                 cmd_help),
    ({"what", "can", "you"},   cmd_help),
]


def dispatch(text: str, speaker: Speaker) -> bool:
    """
    Match *text* against known commands and execute the first match.
    Returns False if the user asked to quit, True otherwise.
    """
    if not text:
        return True

    # Quit commands
    if any(word in text for word in ("quit", "exit", "stop", "bye", "goodbye")):
        speaker.say("Goodbye! Have a great day.")
        return False

    # Try each registered command
    for keywords, handler in COMMANDS:
        if all(kw in text for kw in keywords):
            handler(speaker, text)
            return True

    # No match
    speaker.say("I didn't understand that. Say 'help' for a list of commands.")
    return True


# ---------------------------------------------------------------------------
# 5.  Main loop
# ---------------------------------------------------------------------------
def main():
    parser = argparse.ArgumentParser(description="Mini Voice AI Assistant")
    parser.add_argument(
        "--text", action="store_true",
        help="Use text input instead of microphone",
    )
    args = parser.parse_args()

    use_mic = not args.text and MIC_AVAILABLE

    # Banner
    print("=" * 60)
    print("  🎙️   Voice AI Assistant — Day 13")
    print("=" * 60)

    if use_mic:
        print("  Mode : 🎤  Microphone (Google Speech Recognition)")
    else:
        if not args.text and not MIC_AVAILABLE:
            print("  ⚠️   PyAudio not found — falling back to text mode.")
            print("       Install it with: pip install pyaudio")
        print("  Mode : ⌨️   Text input")

    print("  TTS  :", "✅  pyttsx3" if TTS_AVAILABLE else "❌  unavailable")
    print("  Say 'help' for available commands, 'quit' to exit.")
    print("=" * 60)

    speaker = Speaker()
    recognizer = sr.Recognizer()

    speaker.say("Voice assistant ready. How can I help you?")

    running = True
    while running:
        if use_mic:
            text = listen_from_mic(recognizer)
        else:
            text = listen_from_keyboard()

        running = dispatch(text, speaker)

    print("\n👋  Assistant stopped.")
if __name__ == "__main__":
    main()
