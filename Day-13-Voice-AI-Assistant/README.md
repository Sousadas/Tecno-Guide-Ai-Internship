# Day 13 — Voice AI Assistant

## Summary
A mini voice AI assistant built with Python that listens to spoken commands via the microphone, converts speech to text using Google's Web Speech API, executes voice commands, and responds with spoken output using pyttsx3 (offline TTS).

## Features
- 🎤 **Speech Recognition** — real-time microphone input via SpeechRecognition + PyAudio
- 🔊 **Text-to-Speech** — offline spoken responses via pyttsx3
- ⌨️ **Text Fallback** — works without a microphone using keyboard input
- 🧠 **10 Voice Commands** — greet, time, date, search, open websites, jokes, math, system info, help, quit
- 🛡️ **Error Handling** — graceful handling of timeouts, unrecognized speech, and API errors

## Dependencies
```bash
pip install SpeechRecognition pyttsx3 pyaudio
```

> **macOS note**: install PortAudio first: `brew install portaudio`

## Tasks / Deliverables
- `voice_assistant.py` — main voice assistant script
- `notes.md` — study notes and learnings
- `screenshots/` — demo screenshots

## How to Run

### Microphone mode (default)
```bash
python voice_assistant.py
```

### Text-input mode (no mic needed)
```bash
python voice_assistant.py --text
```

## Available Commands
| Say this... | What happens |
|-------------|--------------|
| "hello" / "hi" / "hey" | Friendly greeting |
| "time" | Current time |
| "date" | Today's date |
| "search Python tutorials" | Opens Google search |
| "open YouTube" | Opens the website |
| "tell me a joke" | Programming joke |
| "calculate 12 plus 7" | Basic math (19) |
| "system info" | OS, architecture, Python version |
| "help" | Lists all commands |
| "quit" / "exit" / "bye" | Stops the assistant |
