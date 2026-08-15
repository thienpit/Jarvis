from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import logging
from app.config import HOST, PORT
from app.services.hermes_client import process_with_hermes
from app.services.tts_service import generate_tts

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(title="Jarvis AI Assistant Backend")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class ProcessRequest(BaseModel):
    text: str

class ProcessResponse(BaseModel):
    response: str
    audio_base64: str = ""
    success: bool = True

@app.get("/health")
async def health():
    return {"status": "healthy", "service": "jarvis-backend"}

@app.post("/api/process")
async def process_request(request: ProcessRequest):
    logger.info(f"Processing request: {request.text[:50]}...")
    
    response_text = await process_with_hermes(request.text)
    
    audio_base64 = ""
    try:
        audio_base64 = await generate_tts(response_text)
    except Exception as e:
        logger.warning(f"TTS failed: {e}")
    
    return ProcessResponse(
        response=response_text,
        audio_base64=audio_base64,
        success=True
    )

@app.on_event("startup")
async def startup():
    logger.info("Jarvis backend started")
