# schemas.py

from datetime import datetime
from typing import Annotated, Literal
from pydantic import BaseModel


class ModelRequest(BaseModel):
    prompt: str


class ModelResponse(BaseModel):
    request_id: str
    ip: str | None
    content: str | bytes
    created_at: datetime = datetime.now()


class TextModelRequest(ModelRequest):
    model: Literal["tinyllama", "gemma2b"]
    temperature: float = 0.0


class TextModelResponse(ModelResponse):
    tokens: int


ImageSize = Annotated[tuple[int, int], "Width and height of an image in pixels"]


class ImageModelRequest(ModelRequest):
    model: Literal["tinysd", "sd1.5"]
    output_size: ImageSize
    num_inference_steps: int = 200


class ImageModelResponse(ModelResponse):
    size: ImageSize
    url: str
