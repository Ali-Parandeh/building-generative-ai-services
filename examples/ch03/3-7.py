# models.py

import torch
from diffusers import DiffusionPipeline, StableDiffusionInpaintPipelineLegacy
from PIL import Image

device = torch.device("cuda" if torch.cuda.is_available() else "cpu")


def load_image_model() -> StableDiffusionInpaintPipelineLegacy:
    pipe = DiffusionPipeline.from_pretrained(
        "segmind/tiny-sd", torch_dtype=torch.float32, device=device
    )
    return pipe


def generate_image(
    pipe: StableDiffusionInpaintPipelineLegacy, prompt: str
) -> Image.Image:
    output = pipe(prompt, num_inference_steps=10).images[0]
    return output
