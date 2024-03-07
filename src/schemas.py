from datetime import datetime
from typing import Annotated, Literal

from pydantic import (UUID4, BaseModel, Field, HttpUrl, IPvAnyAddress,
                      PositiveInt)


class ModelRequest(BaseModel):
    prompt: Annotated[str, Field(min=1, max=4000)]


class TextModelRequest(ModelRequest):
    model: Literal["tinyllama", "gemma2b"]
    temperature: Annotated[float, Field(gte=0.0, lte=1.0, default=0.0)]


class ImageModelRequest(ModelRequest):
    model: Literal["tinysd", "dalle"]
    output_size: tuple[PositiveInt, PositiveInt]
    num_inference_steps: PositiveInt = 200


class ModelResponse(BaseModel):
    request_id: UUID4
    ip: IPvAnyAddress
    content: Annotated[str | bytes, Field(min=0, max=5000)]
    created_at: datetime = datetime.now()


class TextModelResponse(ModelResponse):
    tokens: Annotated[int, Field(gte=0)]


class ImageModelResponse(ModelResponse):
    size: tuple[int, int] = tuple[Field(gte=0), Field(gte=0)]
    url: HttpUrl
