# projectx_frontend.py

import gradio as gr
import requests

API_URL = "http://127.0.0.1:8000/chat"

PERSONALITIES = ["Default", "Luna", "Zen", "Rogue", "Teacher"]

def call_backend(user_input, voice_toggle, personality_choice):
    try:
        payload = {
            "user_input": user_input,
            "voice_toggle": voice_toggle,
            "personality_choice": personality_choice
        }
        response = requests.post(API_URL, json=payload)
        return response.json()["response"]
    except Exception as e:
        return f"[Frontend Error: {str(e)}]"

with gr.Blocks() as demo:
    gr.Markdown("## 🤖 Project X Chat (Frontend)")
    user_input = gr.Textbox(label="Your Message")
    voice_toggle = gr.Checkbox(label="Enable Voice")
    personality = gr.Dropdown(choices=PERSONALITIES, label="Personality", value="Default")
    output = gr.Textbox(label="Bot Response")
    btn = gr.Button("Send")

    btn.click(fn=call_backend, inputs=[user_input, voice_toggle, personality], outputs=output)

demo.launch(inbrowser=True)
