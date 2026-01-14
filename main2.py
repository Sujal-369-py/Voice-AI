from groq import Groq
import pyttsx3 
import sounddevice as sd  
from scipy.io.wavfile import write 
from dotenv import load_dotenv 
import os 
import numpy as np

load_dotenv()

client = Groq(api_key=os.getenv("GROQ_API_KEY"))

def speak(text): 
    engine = pyttsx3.init() 
    engine.say(text) 
    engine.runAndWait()


def main():
    fs = 44100
    chunks = []

    def callback(indata, frames, time, status):
        chunks.append(indata.copy())

    print("Recording... Ctrl+C to stop")

    try:
        with sd.InputStream(samplerate=fs, channels=1, callback=callback):
            while True:
                pass
    except KeyboardInterrupt:
        audio = np.concatenate(chunks, axis=0)
        write("saved_file.wav", fs, audio)
        print("Stopped")
        

    transcript = client.audio.translations.create(
        model="whisper-large-v3",
        file=open("saved_file.wav", "rb")
    )

    user_text = transcript.text
    print("Your message:", user_text)

    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages = [
    {
        "role": "system",
        "content": "Reply briefly. Be very specific. Use short sentences only."
    },
    {
        "role": "user",
        "content": user_text
    }
]


    )

    ai_text = response.choices[0].message.content
    print("AI:", ai_text)
    speak(ai_text)


