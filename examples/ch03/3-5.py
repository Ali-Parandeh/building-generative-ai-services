# utils.py

from io import BytesIO
import soundfile
import numpy as np


def audio_array_to_buffer(audio_array: np.array, sample_rate: int) -> BytesIO:
    buffer = BytesIO()
    soundfile.write(buffer, audio_array, sample_rate, format="wav")
    buffer.seek(0)
    return buffer


# main.py

from fastapi import FastAPI, status
from fastapi.responses import StreamingResponse

from models import load_audio_model, generate_audio
from schemas import VoicePresets
from utils import audio_array_to_buffer

app = FastAPI()


@app.get(
    "/generate/audio",
    responses={status.HTTP_200_OK: {"content": {"audio/wav": {}}}},
    response_class=StreamingResponse,
)
def serve_text_to_audio_model_controller(
    prompt: str,
    preset: VoicePresets = "v2/en_speaker_1",
):
    processor, model = load_audio_model()
    output, sample_rate = generate_audio(processor, model, prompt, preset)
    return StreamingResponse(
        audio_array_to_buffer(output, sample_rate), media_type="audio/wav"
    )
