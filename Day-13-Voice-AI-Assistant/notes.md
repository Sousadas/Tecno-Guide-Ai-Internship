# Day 13 Notes — Voice AI Assistant

Date: 2026-05-29

## Objectives
- Use SpeechRecognition library to transcribe audio from the microphone
- Use pyttsx3 for offline text-to-speech (TTS)
- Build a working voice command dispatcher
- Handle errors gracefully (no mic, API failures, unrecognized speech)

## What I learned

### Speech Recognition Basics
- **SpeechRecognition** library provides a unified API for multiple speech engines
- `recognize_google()` uses Google's free Web Speech API (no API key needed)
- `adjust_for_ambient_noise()` calibrates the mic for background noise levels
- `listen()` accepts `timeout` (max wait for speech to start) and `phrase_time_limit` (max recording length)
- Three common exceptions to handle:
  - `WaitTimeoutError` — no speech detected in the timeout window
  - `UnknownValueError` — audio was captured but couldn't be transcribed
  - `RequestError` — the API call failed (network issue, rate limit, etc.)

### Text-to-Speech (pyttsx3)
- **pyttsx3** works entirely offline (uses system TTS engines: NSSpeechSynthesizer on macOS, SAPI5 on Windows, espeak on Linux)
- Properties you can tune: `rate` (words per minute), `volume`, `voice` (choose from installed voices)
- Pattern: `engine.say(text)` → `engine.runAndWait()` (blocking call)

### PyAudio & Microphone Input
- **PyAudio** is the Python binding for **PortAudio** (a cross-platform audio I/O library)
- On macOS you must install the system library first: `brew install portaudio`
- Then: `pip install pyaudio`
- `sr.Microphone()` wraps PyAudio to provide a context-managed audio source

### Voice Command Architecture
- **Keyword-matching dispatcher**: each command is a `(set_of_keywords, handler)` pair
- `dispatch()` iterates through registered commands, checking if ALL keywords appear in the text
- Handlers receive the full transcribed text so they can extract parameters (e.g., search queries, math expressions)
- A **fallback text-input mode** keeps the command logic testable even without a microphone

### Commands Implemented
| Command | Trigger Words | What It Does |
|---------|---------------|--------------|
| Greet | hello, hi, hey | Random friendly greeting |
| Time | time | Tells the current time |
| Date | date | Tells today's date |
| Search | search, look up | Opens Google search in browser |
| Open site | open + site name | Opens YouTube, GitHub, etc. |
| Joke | joke | Tells a programming joke |
| Calculate | calculate, what is | Evaluates basic math expressions |
| System info | system info | Reports OS, architecture, Python version |
| Help | help, what can you | Lists all available commands |
| Quit | quit, exit, bye | Stops the assistant |

## Key Takeaways
1. **Always handle graceful fallbacks** — the text-input mode means the assistant works even without PyAudio
2. **Ambient noise calibration** is critical for real-world mic usage
3. **Google Web Speech API** is free but requires internet; for offline recognition consider CMU Sphinx (`recognize_sphinx`)
4. **pyttsx3** is the easiest offline TTS for Python — no API keys, no network dependency

## Next Steps
- Integrate intent recognition with NLP (spaCy or NLTK) for more flexible command parsing
- Add wake-word detection ("Hey assistant…")
- Explore offline speech recognition with Vosk or Whisper
- Add more commands (weather, reminders, file operations)
