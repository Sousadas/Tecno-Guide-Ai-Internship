# Day 08 — ChatGPT API & Conversational AI Chatbots

Summary:
- Integrate with OpenAI / ChatGPT API using the modern `openai>=1.0.0` client SDK.
- Learn to build multi-turn conversational agents with state persistence.
- Implement both a terminal interface and a highly interactive, responsive Streamlit web application.

## Tasks / Deliverables
- `chatgpt_example.py`: Migrated baseline example demonstrating modern OpenAI SDK integration.
- `chatbot.py`: Interactive command-line chatbot supporting conversation history tracking and real-time streaming output.
- `app.py`: High-fidelity Streamlit web application with custom CSS styling, temperature parameter configuration, system instruction persona presets, and streaming visual feedback.
- `notes.md`: Documentation of learning outcomes, patterns discovered, and core takeaways.

## Running Instructions

### Prerequisites
Make sure your environment is activated and requirements are installed:
```bash
source .venv/bin/activate
pip install -r requirements.txt
```

### 1. Set up your API key
Provide your OpenAI API Key as an environment variable:
```bash
export OPENAI_API_KEY="your-api-key-here"
```

### 2. Run the Command-line Chatbot
Execute the terminal chatbot in interactive mode:
```bash
python Day-08-ChatGPT-API/chatbot.py
```
Type `exit` or `quit` to close the session.

### 3. Run the Streamlit Web Application
Execute the Streamlit web chatbot:
```bash
streamlit run Day-08-ChatGPT-API/app.py
```
*(If you do not have the environment variable configured, you can also paste your API key securely into the sidebar form of the web app).*

