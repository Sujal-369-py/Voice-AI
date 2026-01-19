import streamlit as st
from groq import Groq
from dotenv import load_dotenv
import os
import tempfile

#config
MAX_MEMORY = 15
CHAT_MODEL = "llama-3.3-70b-versatile"
STT_MODEL = "whisper-large-v3"
TTV_MODEL = "canopylabs/orpheus-v1-english"

load_dotenv()
client = Groq(api_key=os.getenv("GROQ_API_KEY"))

st.set_page_config(
    page_title="Voice AI",
    layout="centered"
)

# voice function
def speak(text):
    response = client.audio.speech.create(
        model=TTV_MODEL,
        voice="autumn",          # or autumn / hannah / etc
        input=text,
        response_format="wav"    # REQUIRED
    )

    with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as f:
        f.write(response.read())
        audio_file = f.name

    st.audio(audio_file, format="audio/wav")


# memeory -> Sliding window...
if "messages" not in st.session_state:
    st.session_state.messages = []

# daam UI in streamlit 😂😂
st.title("🎙️ Voice AI")
st.caption("Speak. Remember. Respond.")

# show chat history
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

audio = st.audio_input("Hold to record and release")

# ---------- logic ----------
if audio:
    with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as f:
        f.write(audio.getbuffer())
        audio_path = f.name

    with st.spinner("Transcribing"):
        transcript = client.audio.transcriptions.create(
            model=STT_MODEL,
            file=open(audio_path, "rb")
        )

    user_text = transcript.text

    # save user message
    st.session_state.messages.append(
        {"role": "user", "content": user_text}
    )
    st.session_state.messages = st.session_state.messages[-MAX_MEMORY:]

    with st.chat_message("user"):
        st.markdown(user_text)

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

    # save assistant message
    st.session_state.messages.append(
        {"role": "assistant", "content": ai_text}
    )
    st.session_state.messages = st.session_state.messages[-MAX_MEMORY:]

    with st.chat_message("assistant"):
        st.markdown(ai_text)

    speak(ai_text)
