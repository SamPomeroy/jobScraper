
import os
import requests
from typing import Optional
import logging
from dotenv import load_dotenv
from pathlib import Path
from fastapi import FastAPI, Header, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from threading import Thread
from datetime import datetime
from supabase import create_client
from langchain_chroma import Chroma
from langchain_ollama import OllamaEmbeddings, ChatOllama
from jose import jwt
import pyttsx3
from gtts import gTTS
import time


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


env_path = Path(__file__).parent / ".env"
load_dotenv(dotenv_path=env_path)

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")
N8N_WEBHOOK = os.getenv("N8N_WEBHOOK")
N8N_SECRET = os.getenv("N8N_SECRET")

supabase = create_client(SUPABASE_URL, SUPABASE_KEY) if SUPABASE_URL and SUPABASE_KEY else None


try:
    vectorstore = Chroma(persist_directory="db", embedding_function=OllamaEmbeddings(model="nomic-embed-text"))
    logger.info("Vector store initialized successfully")
except Exception as e:
    logger.error(f"Vector store initialization failed: {e}")
    vectorstore = None


try:
    llm = ChatOllama(model="llama3.2:1b", base_url="http://127.0.0.1:11500")
    logger.info("Ollama LLM initialized successfully")
except Exception as e:
    logger.error(f"Ollama LLM initialization failed: {e}")
    llm = None

# ✅ FastAPI App Setup
app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
@app.post("/api/generate")
async def generate():
    return {"message": "API is working!"}

def verify_token(auth: str):
    """Verify authorization token"""
    if not auth or not auth.startswith("Bearer"):
        raise HTTPException(status_code=401, detail="Missing token")
    
    try:
        token = auth.split()[1]
        payload = jwt.get_unverified_claims(token)
        return payload["sub"]
    except Exception:
        raise HTTPException(status_code=401, detail="Invalid token")

def generate_audio(user_id: str, reply_text: str) -> str:
    """Generates and saves voice response"""
    audio_file = f"static/{user_id}_response.mp3"

    if not os.path.exists(audio_file):  
        tts = gTTS(reply_text)
        tts.save(audio_file)

    return audio_file


def upload_audio_to_supabase(user_id: str, audio_file: str) -> Optional[str]:
    """Uploads generated speech to Supabase Storage"""
    try:
        with open(audio_file, "rb") as f:
            file_data = f.read()

        response = supabase.storage.from_("audio_responses").upload(
            f"{user_id}/response.mp3", file_data, {"content-type": "audio/mpeg"}
        )

        if response.status_code == 200:
            logger.info(f"Uploaded voice response for {user_id} successfully.")
            return f"https://YOUR_SUPABASE_URL/storage/v1/object/public/audio_responses/{user_id}/response.mp3"
        else:
            logger.error(f"Error uploading audio: {response.json()}")
            return None
    except Exception as e:
        logger.error(f"Supabase upload failed: {e}")
        return None


@app.get("/chat_voice")
async def chat_voice_endpoint(query: str = Query(...), authorization: Optional[str] = Header(None)):
    """Dedicated voice chat handler with Supabase storage"""
    logger.info(f"Received voice chat request: {query}")

    user_id = "anonymous"
    if authorization:
        try:
            user_id = verify_token(authorization)
        except HTTPException:
            user_id = "anonymous"

    prompt = f"User: {query}\nAssistant:"
    reply_text = get_ollama_response(prompt)

    audio_file = generate_audio(user_id, reply_text)  
    audio_url = upload_audio_to_supabase(user_id, audio_file)

    return {"response": reply_text, "audio": audio_url if audio_url else audio_file}


def store_to_supabase(user_id: str, user_message: str, assistant_reply: str):
    if not supabase:
        logger.warning("Supabase not configured, skipping storage")
        return

    try:
        supabase.table("chat_history").insert([
            {"user_id": user_id, "role": "user", "message": user_message, "timestamp": datetime.utcnow().isoformat()},
            {"user_id": user_id, "role": "assistant", "message": assistant_reply, "timestamp": datetime.utcnow().isoformat()}
        ]).execute()
    except Exception as e:
        logger.error(f"Error storing to Supabase: {e}")

def get_ollama_response(prompt: str) -> str:
    """Sends a request to Ollama and returns the response"""
    if not llm:
        logger.error("LLM not initialized")
        return "AI model is not available right now."

    try:
        logger.info(f"Sending prompt to Ollama: {prompt}")
        response = requests.post(
            "http://127.0.0.1:11500/api/generate",
            headers={"Content-Type": "application/json"},
            json={"model": "mistral", "prompt": prompt, "stream": False}
        )
        response.raise_for_status()
        result = response.json()

        if "response" in result:
            return result["response"]
        else:
            return "Unexpected response format from Ollama."

    except requests.exceptions.RequestException as e:
        logger.error(f"Error connecting to Ollama: {e}")
        return "I'm having trouble processing your request right now."
    
@app.get("/chat")
async def chat_get_endpoint(
    query: str = Query(...), 
    authorization: Optional[str] = Header(None), 
    include_audio: bool = Query(False)
):
    """Handles user chat requests with optional voice response storage"""
    logger.info(f"Received chat request: {query}")
    
    user_id = "anonymous"
    if authorization:
        try:
            user_id = verify_token(authorization)
        except HTTPException:
            user_id = "anonymous"


    prior = ""
    if user_id != "anonymous" and supabase:
        try:
            history_response = supabase.table("chat_history").select("role,message") \
                .eq("user_id", user_id).order("timestamp", desc=False).limit(10).execute()
            prior = "\n".join(f"{m['role']}: {m['message']}" for m in history_response.data or [])
        except Exception as e:
            logger.error(f"Error fetching history: {e}")

  
    context = ""
    if vectorstore:
        try:
            docs = vectorstore.similarity_search(query, k=3)
            context = "\n".join(doc.page_content for doc in docs)
        except Exception as e:
            logger.error(f"Vector search error: {e}")

   
    prompt = f"""You're a helpful learning assistant.\n\nPast conversation:\n{prior}\n\nRelevant background info:\n{context}\n\nUser: {query}\nAssistant:"""
    reply_text = get_ollama_response(prompt)


    audio_file = None
    audio_url = None
    if include_audio:
        audio_file = generate_audio(user_id, reply_text)
        audio_url = upload_audio_to_supabase(user_id, audio_file)

  
    if user_id != "anonymous":
        Thread(target=store_to_supabase, args=(user_id, query, reply_text)).start()
        Thread(target=log_to_n8n,
               args=(user_id, query, reply_text)).start()

    return {"response": reply_text, "audio": audio_url}

@app.get("/chat-history")
async def chat_history(user_id: str = Query(...), authorization: str = Header(...)):
    """Fetch chat history for a user"""
    if not supabase:
        return {"history": [], "message": "Database not configured"}

    token_id = verify_token(authorization)
    if token_id != user_id:
        raise HTTPException(status_code=403, detail="Forbidden")

    try:
        res = supabase.table("chat_history") \
            .select("role,message,timestamp") \
            .eq("user_id", user_id) \
            .order("timestamp", desc=False).limit(20).execute()
        return {"history": res.data or []}
    except Exception as e:
        logger.error(f"Error fetching history: {e}")
        return {"history": [], "error": str(e)}

        
def log_to_n8n(user_id: str, user_message: str, assistant_reply: str):
    if not N8N_WEBHOOK or not N8N_SECRET:
        logger.warning("n8n not configured, skipping logging")
        return

    try:
        payload = {
            "user_id": user_id,
            "message": user_message,
            "role": "assistant",
            "reply": assistant_reply,
            "timestamp": datetime.utcnow().isoformat()
        }
        headers = {"Authorization": f"Bearer {N8N_SECRET}", "Content-Type": "application/json"}
        response = requests.post(N8N_WEBHOOK, json=payload, headers=headers, timeout=10)
        response.raise_for_status()
        logger.info(f"Logged to n8n successfully for user {user_id}")
    except Exception as e:
        logger.error(f"n8n logging failed: {e}")

@app.get("/health")
async def health_check():
    ollama_status = "healthy" if llm else "not initialized"
    return {
        "status": "healthy",
        "ollama": ollama_status,
        "supabase": "configured" if supabase else "not configured",
        "vectorstore": "configured" if vectorstore else "not configured"
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)

