# main.py
from fastapi import FastAPI, status
from fastapi.responses import StreamingResponse

from models import load_3d_model, generate_3d_geometry
from utils import mesh_to_obj_buffer

app = FastAPI()


@app.get(
    "/generate/3d",
    responses={status.HTTP_200_OK: {"content": {"model/obj": {}}}},
    response_class=StreamingResponse,
)
def serve_text_to_3d_model_controller(
    prompt: str, num_inference_steps: int = 25
):
    model = load_3d_model()
    mesh = generate_3d_geometry(model, prompt, num_inference_steps)
    response = StreamingResponse(
        mesh_to_obj_buffer(mesh), media_type="model/obj"
    )
    response.headers["Content-Disposition"] = (
        f"attachment; filename={prompt}.obj"
    )
    return response
