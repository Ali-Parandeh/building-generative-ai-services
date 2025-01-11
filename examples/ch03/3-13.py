# models.py
import torch
from diffusers import ShapEPipeline

device = torch.device("cuda" if torch.cuda.is_available() else "cpu")


def load_3d_model() -> ShapEPipeline:
    pipe = ShapEPipeline.from_pretrained("openai/shap-e", device=device)
    return pipe


def generate_3d_geometry(
    pipe: ShapEPipeline, prompt: str, num_inference_steps: int
):
    images = pipe(
        prompt,
        guidance_scale=15.0,
        num_inference_steps=num_inference_steps,
        output_type="mesh",
    ).images[0]
    return images
