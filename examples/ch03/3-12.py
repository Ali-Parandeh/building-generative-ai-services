# main.py

from fastapi import status, FastAPI, File
from fastapi.responses import StreamingResponse
from io import BytesIO
from PIL import Image

from models import load_video_model, generate_video
from utils import export_to_video_buffer

app = FastAPI()


@app.post(
    "/generate/video",
    responses={status.HTTP_200_OK: {"content": {"video/mp4": {}}}},
    response_class=StreamingResponse,
)
def serve_image_to_video_model_controller(
    image: bytes = File(...), num_frames: int = 25
):
    image = Image.open(BytesIO(image))
    model = load_video_model()
    frames = generate_video(model, image, num_frames)
    return StreamingResponse(
        export_to_video_buffer(frames), media_type="video/mp4"
    )
