import streamlit as st
from groq import Groq
from dotenv import load_dotenv
from gtts import gTTS
import os
import tempfile

# ---------- config ----------
MAX_MEMORY = 15
CHAT_MODEL = "llama-3.3-70b-versatile"
STT_MODEL = "whisper-large-v3"

# ---------- setup ----------
load_dotenv()

api_key = os.getenv("GROQ_API_KEY") or st.secrets["GROQ_API_KEY"]
client = Groq(api_key=api_key)

st.set_page_config(
    page_title="Voice AI",
    layout="centered"
)

# ---------- memory ----------
if "messages" not in st.session_state:
    st.session_state.messages = []

# ---------- UI ----------
st.title("🎙️ Voice AI")
st.caption("Speak. Remember. Respond.")

# show chat history
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

audio = st.audio_input("Hold to record and release")

# ---------- logic ----------
if audio:
    # save input audio
    with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as f:
        f.write(audio.getbuffer())
        audio_path = f.name

    # STT
    with st.spinner("Transcribing"):
        transcript = client.audio.transcriptions.create(
            model=STT_MODEL,
            file=open(audio_path, "rb")
        )

    user_text = transcript.text

    # store user message
    st.session_state.messages.append(
        {"role": "user", "content": user_text}
    )
    st.session_state.messages = st.session_state.messages[-MAX_MEMORY:]

    with st.chat_message("user"):
        st.markdown(user_text)

    # LLM
    with st.spinner("Thinking"):
        response = client.chat.completions.create(
            model=CHAT_MODEL,
            messages=[
                {
                    "role": "system",
                    "content": (
                        "Reply in a natural, conversational way. "
                        "Keep responses concise but meaningful. "
                        "Avoid very long answers."
                    )
                },
                *st.session_state.messages
            ]
        )

    ai_text = response.choices[0].message.content

    # store assistant message
    st.session_state.messages.append(
        {"role": "assistant", "content": ai_text}
    )
    st.session_state.messages = st.session_state.messages[-MAX_MEMORY:]

    with st.chat_message("assistant"):
        st.markdown(ai_text)

    # ---------- browser TTS ----------
    tts = gTTS(text=ai_text, lang="en")
    with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as audio_out:
        tts.save(audio_out.name)
        st.audio(audio_out.name, format="audio/mp3")
