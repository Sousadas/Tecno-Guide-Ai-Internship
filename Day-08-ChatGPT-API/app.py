import os
import json
import uuid
from datetime import datetime
import streamlit as st
from dotenv import load_dotenv
from openai import OpenAI
from google import genai
from google.genai import types

# Load environment variables from .env file
load_dotenv()

# ----------------------------------------------------
# 1. Page Configuration & Custom CSS
# ----------------------------------------------------
st.set_page_config(
    page_title="AI Chatbot",
    page_icon="💬",
    layout="centered",
    initial_sidebar_state="expanded"
)

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600&display=swap');

html, body, [class*="css"], .stMarkdown, .stTextInput, .stSelectbox {
    font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif !important;
}

#MainMenu {visibility: hidden;}
footer {visibility: hidden;}

/* Keep sidebar toggle visible but hide the deploy button */
[data-testid="stToolbar"] {visibility: hidden;}


.block-container {
    padding-top: 1.5rem !important;
    max-width: 820px !important;
}

/* ---- Header ---- */
.app-header {
    text-align: center;
    padding: 0.5rem 0 1.2rem 0;
    border-bottom: 1px solid rgba(255,255,255,0.06);
    margin-bottom: 1rem;
}
.app-header h1 {
    font-size: 1.3rem;
    font-weight: 600;
    color: #e2e8f0;
    margin: 0;
    letter-spacing: -0.02em;
}
.app-header p {
    font-size: 0.78rem;
    color: #64748b;
    margin: 0.25rem 0 0 0;
    font-weight: 300;
}
.provider-badge {
    display: inline-block;
    font-size: 0.68rem;
    font-weight: 500;
    color: #94a3b8;
    background: rgba(255,255,255,0.05);
    border: 1px solid rgba(255,255,255,0.08);
    border-radius: 20px;
    padding: 0.15rem 0.6rem;
    margin-top: 0.4rem;
    letter-spacing: 0.03em;
}

/* ---- Chat messages ---- */
.stChatMessage {
    border-radius: 10px !important;
    border: none !important;
    margin-bottom: 0.3rem !important;
    animation: msgSlide 0.25s ease-out;
}
@keyframes msgSlide {
    from { opacity: 0; transform: translateY(5px); }
    to   { opacity: 1; transform: translateY(0); }
}

/* ---- Sidebar ---- */
section[data-testid="stSidebar"] {
    border-right: 1px solid rgba(255,255,255,0.04);
}
section[data-testid="stSidebar"] .stSelectbox label,
section[data-testid="stSidebar"] .stSlider label,
section[data-testid="stSidebar"] .stTextArea label,
section[data-testid="stSidebar"] .stTextInput label {
    font-size: 0.8rem !important;
    font-weight: 500 !important;
    color: #94a3b8 !important;
}

.sidebar-section {
    font-size: 0.7rem;
    font-weight: 600;
    color: #64748b;
    text-transform: uppercase;
    letter-spacing: 0.08em;
    margin: 1rem 0 0.4rem 0;
}

/* Conversation list items */
.conv-item {
    display: flex;
    align-items: center;
    gap: 0.5rem;
    padding: 0.5rem 0.65rem;
    border-radius: 8px;
    margin-bottom: 2px;
    cursor: pointer;
    transition: background 0.15s ease;
    font-size: 0.82rem;
    color: #cbd5e1;
    border: 1px solid transparent;
}
.conv-item:hover {
    background: rgba(255,255,255,0.05);
}
.conv-item.active {
    background: rgba(255,255,255,0.07);
    border-color: rgba(255,255,255,0.08);
    color: #f1f5f9;
}
.conv-icon {
    font-size: 0.9rem;
    flex-shrink: 0;
}
.conv-title {
    overflow: hidden;
    text-overflow: ellipsis;
    white-space: nowrap;
    flex: 1;
}
.conv-time {
    font-size: 0.65rem;
    color: #475569;
    flex-shrink: 0;
}

.empty-state {
    text-align: center;
    color: #475569;
    font-size: 0.8rem;
    padding: 3rem 1rem;
}
.empty-state .icon {
    font-size: 2rem;
    margin-bottom: 0.5rem;
}
.empty-state p {
    margin: 0.3rem 0;
}

.stChatInput {
    border-top: 1px solid rgba(255,255,255,0.06) !important;
}
</style>
""", unsafe_allow_html=True)

# ----------------------------------------------------
# 2. Session State Initialization
# ----------------------------------------------------
# conversations: dict of {id: {title, messages, created_at, provider, model}}
if "conversations" not in st.session_state:
    st.session_state.conversations = {}
if "active_conv" not in st.session_state:
    st.session_state.active_conv = None
if "messages" not in st.session_state:
    st.session_state.messages = []


def new_conversation():
    """Create a new conversation and set it as active."""
    conv_id = str(uuid.uuid4())[:8]
    st.session_state.conversations[conv_id] = {
        "title": "New chat",
        "messages": [],
        "created_at": datetime.now().strftime("%H:%M"),
        "provider": provider,
        "model": selected_model
    }
    st.session_state.active_conv = conv_id
    st.session_state.messages = []
    return conv_id


def switch_conversation(conv_id):
    """Switch to an existing conversation."""
    st.session_state.active_conv = conv_id
    conv = st.session_state.conversations[conv_id]
    st.session_state.messages = conv["messages"].copy()


def delete_conversation(conv_id):
    """Delete a conversation."""
    if conv_id in st.session_state.conversations:
        del st.session_state.conversations[conv_id]
    if st.session_state.active_conv == conv_id:
        st.session_state.active_conv = None
        st.session_state.messages = []


def auto_title(user_msg):
    """Generate a short title from the first user message."""
    title = user_msg.strip()
    if len(title) > 35:
        title = title[:35] + "…"
    return title


# ----------------------------------------------------
# 3. Sidebar
# ----------------------------------------------------

# -- New Chat button --
if st.sidebar.button("＋  New Chat", use_container_width=True, type="primary"):
    # Will be created after provider/model are set below
    st.session_state._pending_new = True

# -- Conversations list --
st.sidebar.markdown('<div class="sidebar-section">Conversations</div>', unsafe_allow_html=True)

conv_ids = list(st.session_state.conversations.keys())
if conv_ids:
    for cid in reversed(conv_ids):  # newest first
        conv = st.session_state.conversations[cid]
        is_active = (cid == st.session_state.active_conv)
        cols = st.sidebar.columns([5, 1])
        with cols[0]:
            label = f"💬 {conv['title']}"
            if st.button(label, key=f"conv_{cid}", use_container_width=True,
                         type="primary" if is_active else "secondary"):
                switch_conversation(cid)
                st.rerun()
        with cols[1]:
            if st.button("🗑", key=f"del_{cid}", help="Delete this chat"):
                delete_conversation(cid)
                st.rerun()
else:
    st.sidebar.caption("No conversations yet. Click **New Chat** to start.")

# -- Divider --
st.sidebar.markdown("---")

# -- Provider --
st.sidebar.markdown('<div class="sidebar-section">Provider</div>', unsafe_allow_html=True)
provider = st.sidebar.selectbox(
    "AI Engine", ["Google Gemini", "OpenAI"],
    label_visibility="collapsed"
)

# API Key handling
api_key = ""
env_openai_key = os.getenv("OPENAI_API_KEY")
env_gemini_key = os.getenv("GEMINI_API_KEY")
if env_openai_key == "insira_sua_chave_aqui":
    env_openai_key = None
if env_gemini_key == "insira_sua_chave_aqui":
    env_gemini_key = None

if provider == "OpenAI":
    if not env_openai_key:
        api_key = st.sidebar.text_input("OpenAI API Key", type="password")
    else:
        api_key = env_openai_key
        st.sidebar.caption("✓ Key loaded from `.env`")
else:
    if not env_gemini_key:
        api_key = st.sidebar.text_input("Gemini API Key", type="password")
    else:
        api_key = env_gemini_key
        st.sidebar.caption("✓ Key loaded from `.env`")

# -- Persona --
st.sidebar.markdown('<div class="sidebar-section">Persona</div>', unsafe_allow_html=True)
presets = {
    "Assistant": "You are a helpful, concise, and friendly AI assistant.",
    "Creative Writer": "You are a creative writer. Use rich metaphors and imaginative language.",
    "Code Expert": "You are an expert software engineer. Write clean code and explain precisely.",
    "Sarcastic": "You are witty and slightly sarcastic. Keep it playful.",
    "Custom": ""
}
selected_preset = st.sidebar.selectbox("Persona", list(presets.keys()), index=0, label_visibility="collapsed")
if selected_preset == "Custom":
    system_prompt = st.sidebar.text_area("Instructions", value="You are an AI assistant.", height=70, label_visibility="collapsed")
else:
    system_prompt = presets[selected_preset]

# -- Model --
st.sidebar.markdown('<div class="sidebar-section">Model</div>', unsafe_allow_html=True)
if provider == "OpenAI":
    selected_model = st.sidebar.selectbox("Model", ["gpt-4o-mini", "gpt-4o"], label_visibility="collapsed")
else:
    selected_model = st.sidebar.selectbox("Model", ["gemini-2.5-flash", "gemini-2.5-pro"], label_visibility="collapsed")

temperature = st.sidebar.slider("Temperature", 0.0, 1.5, 0.7, 0.1)

# Handle pending new chat (after provider/model are defined)
if getattr(st.session_state, "_pending_new", False):
    new_conversation()
    st.session_state._pending_new = False
    st.rerun()

# ----------------------------------------------------
# 4. Main Header
# ----------------------------------------------------
prov_label = "Gemini" if provider == "Google Gemini" else "OpenAI"
st.markdown(f"""
<div class="app-header">
    <h1>AI Chatbot</h1>
    <p>Streaming responses · Multi-provider</p>
    <div class="provider-badge">{prov_label} · {selected_model}</div>
</div>
""", unsafe_allow_html=True)

# ----------------------------------------------------
# 5. Chat Display
# ----------------------------------------------------
# Show empty state if no active conversation
if not st.session_state.active_conv or not st.session_state.messages:
    if not st.session_state.active_conv:
        st.markdown("""
        <div class="empty-state">
            <div class="icon">💬</div>
            <p><strong>Start a new conversation</strong></p>
            <p>Click <b>New Chat</b> in the sidebar to begin.</p>
        </div>
        """, unsafe_allow_html=True)

# Display conversation messages
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# ----------------------------------------------------
# 6. Chat Logic
# ----------------------------------------------------
if not api_key:
    if st.session_state.active_conv:
        st.caption("Enter your API key in the sidebar to begin chatting.")
else:
    if prompt := st.chat_input("Message…"):
        # Auto-create a conversation if none is active
        if not st.session_state.active_conv:
            new_conversation()

        with st.chat_message("user"):
            st.markdown(prompt)
        st.session_state.messages.append({"role": "user", "content": prompt})

        # Auto-title from first message
        conv = st.session_state.conversations[st.session_state.active_conv]
        if conv["title"] == "New chat":
            conv["title"] = auto_title(prompt)

        with st.chat_message("assistant"):
            placeholder = st.empty()
            try:
                if provider == "OpenAI":
                    client = OpenAI(api_key=api_key)
                    payload = [{"role": "system", "content": system_prompt}] + [
                        {"role": m["role"], "content": m["content"]} for m in st.session_state.messages
                    ]
                    stream = client.chat.completions.create(
                        model=selected_model, messages=payload,
                        temperature=temperature, stream=True
                    )
                    full = ""
                    for chunk in stream:
                        c = chunk.choices[0].delta.content
                        if c:
                            full += c
                            placeholder.markdown(full + "▌")
                    placeholder.markdown(full)
                else:
                    client = genai.Client(api_key=api_key)
                    contents_payload = []
                    for m in st.session_state.messages:
                        role_val = "model" if m["role"] == "assistant" else "user"
                        contents_payload.append(
                            types.Content(
                                role=role_val,
                                parts=[types.Part.from_text(text=m["content"])]
                            )
                        )
                    stream = client.models.generate_content_stream(
                        model=selected_model,
                        contents=contents_payload,
                        config=types.GenerateContentConfig(
                            system_instruction=system_prompt,
                            temperature=temperature
                        )
                    )
                    full = ""
                    for chunk in stream:
                        c = chunk.text
                        if c:
                            full += c
                            placeholder.markdown(full + "▌")
                    placeholder.markdown(full)

                st.session_state.messages.append({"role": "assistant", "content": full})
                # Sync back to conversation store
                conv["messages"] = st.session_state.messages.copy()

            except Exception as e:
                placeholder.error(f"Error: {e}")
                st.session_state.messages.pop()
                conv["messages"] = st.session_state.messages.copy()
