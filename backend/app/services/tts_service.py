import asyncio
import base64
import edge_tts
import os
import logging
from app.config import TTS_VOICE

logger = logging.getLogger(__name__)

async def generate_tts(text: str) -> str:
    """
    Generate audio từ text dùng Edge TTS.
    Trả về base64 encoded string của file MP3.
    """
    try:
        communicate = edge_tts.Communicate(text, TTS_VOICE)
        temp_path = "/tmp/jarvis_response.mp3"
        await communicate.save(temp_path)
        
        with open(temp_path, "rb") as f:
            audio_data = f.read()
            audio_base64 = base64.b64encode(audio_data).decode('utf-8')
        
        os.remove(temp_path)
        return audio_base64
        
    except Exception as e:
        logger.error(f"TTS generation failed: {e}")
        return ""
