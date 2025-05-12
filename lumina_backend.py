import asyncio
from fastapi import FastAPI, HTTPException, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from contextlib import contextmanager
from concurrent.futures import ThreadPoolExecutor
import httpx, os, time, sqlite3

# === CONFIGURATION ===
USE_OPENAI = False
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
DB_PATH = "projectx_memory.db"
executor = ThreadPoolExecutor()

PERSONALITIES = {
    "Default": "You are Project X, an AI that helps users online.",
    "Luna": "You are Luna, a cheerful assistant who loves science and space.",
    "Zen": "You are Zen, a calm and philosophical thinker offering deep insights.",
    "Rogue": "You are Rogue, witty and rebellious, always thinking outside the box.",
    "Teacher": "You are a patient and intelligent tutor that explains concepts clearly."
}
DEFAULT_PERSONALITY = PERSONALITIES["Default"]

# === DATABASE ===
@contextmanager
def db_connection():
    conn = sqlite3.connect(DB_PATH)
    try:
        yield conn
    finally:
        conn.close()

def setup_database():
    with db_connection() as conn:
        conn.execute("""
            CREATE TABLE IF NOT EXISTS memory (
                id INTEGER PRIMARY KEY,
                timestamp TEXT,
                user_input TEXT,
                bot_response TEXT
            )
        """)
        conn.commit()

setup_database()

def store_in_memory(user_input, bot_response):
    with db_connection() as conn:
        conn.execute(
            "INSERT INTO memory (timestamp, user_input, bot_response) VALUES (?, ?, ?)",
            (time.ctime(), user_input, bot_response)
        )
        conn.commit()

def retrieve_memory():
    with db_connection() as conn:
        result = conn.execute(
            "SELECT user_input, bot_response FROM memory ORDER BY id DESC LIMIT 10"
        ).fetchall()
    memory_str = "\n".join([f"You: {u}\nBot: {b}" for u, b in result])
    return memory_str[-1000:] if len(memory_str) > 1000 else memory_str

def is_online():
    try:
        httpx.get("https://api.openai.com", timeout=6.0)
        return True
    except:
        return False

async def ask_openai(prompt, personality):
    try:
        headers = {
            "Authorization": f"Bearer {OPENAI_API_KEY}",
            "Content-Type": "application/json"
        }
        data = {
            "model": "gpt-3.5-turbo",
            "messages": [
                {"role": "system", "content": personality},
                {"role": "user", "content": prompt}
            ]
        }
        async with httpx.AsyncClient() as client:
            response = await client.post("https://api.openai.com/v1/chat/completions", headers=headers, json=data)
        return response.json()['choices'][0]['message']['content']
    except Exception as e:
        return f"[OpenAI error: {str(e)}]"

async def ask_ollama(prompt):
    try:
        data = {
            "model": "llama3",
            "prompt": prompt,
            "stream": True
        }
        async with httpx.AsyncClient() as client:
            response = await client.post("http://localhost:11434/v1/generate", json=data)  # Example endpoint
        return response.json().get("response", "[No response from local model]")
    except Exception as e:
        return f"[Ollama error: {str(e)}]"


async def chat(user_input, personality_choice):
    personality = PERSONALITIES.get(personality_choice, DEFAULT_PERSONALITY)
    loop = asyncio.get_event_loop()

    # Run both functions in parallel using the thread pool
    memory_task = loop.run_in_executor(executor, retrieve_memory)
    online_task = loop.run_in_executor(executor, is_online)

    memory_context, online_status = await asyncio.gather(memory_task, online_task)

    prompt = f"Recent memory:\n{memory_context}\n\nUser: {user_input}\nAI:"

    if online_status and USE_OPENAI:
        response = await ask_openai(prompt, personality)
    else:
        response = await ask_ollama(prompt)

    return response

# === FASTAPI APP ===
app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class ChatRequest(BaseModel):
    user_input: str
    voice_toggle: bool  # Currently unused
    personality_choice: str

@app.post("/chat")
async def chatbot(request: ChatRequest, background_tasks: BackgroundTasks):
    result = await chat(request.user_input, request.personality_choice)

    background_tasks.add_task(store_in_memory, request.user_input, result)

    if not result:
        raise HTTPException(status_code=400, detail="Chatbot failed to generate a response.")
    return {"response": result}


# Run with:
# uvicorn lumina_backend:app --reload
