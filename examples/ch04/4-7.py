# schemas.py

from datetime import datetime
from uuid import uuid4
from typing import Annotated, Literal

from pydantic import BaseModel, Field, HttpUrl, IPvAnyAddress, PositiveInt


class ModelRequest(BaseModel):
    prompt: Annotated[str, Field(min_length=1, max_length=10000)]


class ModelResponse(BaseModel):
    request_id: Annotated[str, Field(default_factory=lambda: uuid4().hex)]
    # no defaults set for ip field
    # raises ValidationError if a valid IP address or None is not provided.
    ip: Annotated[str, IPvAnyAddress] | None
    content: Annotated[str | bytes, Field(min_length=0, max_length=10000)]
    created_at: datetime = datetime.now()


class TextModelRequest(ModelRequest):
    model: Literal["tinyllama", "gemma2b"]
    temperature: Annotated[float, Field(ge=0.0, le=1.0, default=0.0)]


class TextModelResponse(ModelResponse):
    tokens: Annotated[int, Field(ge=0)]


ImageSize = Annotated[tuple[PositiveInt, PositiveInt], "Width and height of an image in pixels"]


class ImageModelRequest(ModelRequest):
    model: Literal["tinysd", "sd1.5"]
    output_size: ImageSize
    num_inference_steps: Annotated[int, Field(ge=0, le=2000)] = 200


class ImageModelResponse(ModelResponse):
    size: ImageSize
    url: Annotated[str, HttpUrl] | None = None
