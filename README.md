# 🎙️ Voice AI Assistant

A **voice-first conversational AI** built with Streamlit and Groq.  
🎤 Speak naturally → 🤖 AI responds → 🧠 Remembers context.

---

## ✨ Features
🎙️ Voice input (📱 mobile + 💻 desktop)  
📝 Speech-to-Text using Groq Whisper  
🤖 Chat powered by Groq LLaMA  
🧠 Sliding window memory (last 15 messages)  
💬 Chat history UI  
🚫 No backend server  
📱 Mobile friendly  

---

## 🏗️ Architecture
👤 User (Browser / Phone)  
→ 🖥️ Streamlit UI  
→ 🎙️ Browser Microphone  
→ 📝 Groq Whisper (STT)  
→ 🧠 Sliding Window Memory (15)  
→ 🤖 Groq LLaMA (Chat)  
→ 💬 Text Response  
→ 🔊 Optional Desktop TTS  

---

## 🧠 Memory Design
• Keeps only last **15 messages**  
• Older context is forgotten  
• Controls token cost  
• Feels natural  

Example  
[M1 … M15] → new message  
[M2 … M16]

---

## 🛠️ Tech Stack
🐍 Python  
🖥️ Streamlit  
⚡ Groq API  
📝 Whisper Large v3  
🤖 LLaMA 3.3 70B  
🔐 dotenv  

---

## 📦 Installation
pip install requirements.txt


---

## 🔑 Environment
Create `.env`
GROQ_API_KEY=your_key_here

---


## ▶️ Run
streamlit run main.py


---

## ⚠️ Constraints
📵 No live mic streaming on mobile  
🔊 TTS works only on desktop  
♻️ Memory resets on refresh  

---

## 💡 Why This Project
• Real user interaction  
• STT + LLM + Memory system  
• UX + infra awareness  
• Cost-aware design  
• Not a CRUD demo  

---

## 🔮 Future
🧠 Memory summarization  
💾 Persistent storage  
🔁 Model fallback  
🎧 WebAudio streaming  

---

📄 MIT License  
Built to learn. Shipped to work.
