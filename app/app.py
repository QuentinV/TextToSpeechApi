from fastapi import FastAPI, HTTPException
from fastapi.responses import Response
from pydantic import BaseModel
from typing import Dict
import io
import base64
import wave
from piper.voice import PiperVoice

app = FastAPI()

# Cache of loaded voices
VOICE_CACHE: Dict[str, PiperVoice] = {}

class TTSRequest(BaseModel):
    text: str
    model: str

def load_voice(modelname: str) -> PiperVoice:
    if modelname not in VOICE_CACHE:
        try:
            VOICE_CACHE[modelname] = PiperVoice.load("/app/voices/" + modelname + ".onnx", config_path="/app/voices/" + modelname + ".onnx.json")
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Failed to load model: {e}")
    return VOICE_CACHE[modelname]

@app.post("/tts")
def tts(req: TTSRequest):
    voice = load_voice(req.model)

    chunks = []
    sample_rate = None
    sample_width = None
    channels = None

    # Stream audio chunks
    for chunk in voice.synthesize(req.text):
        if sample_rate is None:
            sample_rate = chunk.sample_rate
            sample_width = chunk.sample_width
            channels = chunk.sample_channels
        chunks.append(chunk.audio_int16_bytes)

    if not chunks:
        raise HTTPException(status_code=500, detail="No audio generated")

    # Build WAV in memory
    buf = io.BytesIO()
    with wave.open(buf, "wb") as wf:
        wf.setnchannels(channels)
        wf.setsampwidth(sample_width)
        wf.setframerate(sample_rate)
        wf.writeframes(b"".join(chunks))

    wav_bytes = buf.getvalue()

    # Return raw WAV response
    return Response(
        content=wav_bytes,
        media_type="audio/wav",
        headers={"Content-Disposition": "inline; filename=speech.wav"}
    )
