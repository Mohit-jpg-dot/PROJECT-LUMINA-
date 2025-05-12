# 🧠 PROJECT LUMINA – Offline AI Chatbot with LLaMA 3 & Mistral

**LUMINA** is a fast, intelligent, and fully offline AI chatbot powered by open-source models like **LLaMA 3** and **Mistral**. Built for privacy and flexibility, it allows natural conversations without needing an internet connection — perfect for developers, students, or anyone who values control over their AI.

## 🚀 Features

- 🌐 **Runs Offline** – Powered by local LLMs via Ollama
- 🤖 **Multi-Model Support** – Easily switch between LLaMA 3 and Mistral
- 🧠 **Smart Conversation** – Context-aware and responsive dialogue
- 🔒 **Privacy First** – No data is sent to the cloud
- 🧩 **Modular & Extendable** – Voice, memory, tools, and more coming soon

## 🔧 Tech Stack

- [LLaMA 3](https://ai.meta.com/llama/)
- [Mistral](https://mistral.ai/)
- [Ollama](https://ollama.com/) – Run LLMs locally
- Python (core framework)

## 📦 Installation

> ✅ Prerequisites: [Ollama](https://ollama.com/download), Python 3.8+

```bash
git clone https://github.com/Mohit-jpg-dot/PROJECT-LUMINA-.git
cd PROJECT-LUMINA-

# Optional: create a virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

First, pull the required model via Ollama:

ollama pull llama3
# or
ollama pull mistral

Then run the chatbot:

python lumina.py
