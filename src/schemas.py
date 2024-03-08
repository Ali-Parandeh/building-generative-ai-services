from datetime import datetime
from typing import Annotated, Literal
from uuid import uuid4

from pydantic import (
    BaseModel,
    Field,
    HttpUrl,
    IPvAnyAddress,
    PositiveInt,
    computed_field,
    field_validator,
    model_validator,
)

from utils import count_tokens


class ModelRequest(BaseModel):
    prompt: Annotated[str, Field(min=1, max=4000)]


class TextModelRequest(ModelRequest):
    model: Literal["tinyllama", "gemma2b"]
    temperature: Annotated[float, Field(gt=0.0, lte=1.0, default=0.01)]


class ImageModelRequest(ModelRequest):
    model: Literal["tinysd", "sd1.5"]
    output_size: tuple[PositiveInt, PositiveInt]
    num_inference_steps: Annotated[int, PositiveInt] = 200

    @field_validator("output_size")
    def validate_output_size(cls, v: tuple[PositiveInt, PositiveInt]) -> tuple[PositiveInt, PositiveInt]:
        if v[0] / v[1] != 1:
            raise ValueError(f"Only square images are supported for {cls.__name__} ")
        if v[0] not in [256, 512]:
            raise ValueError(f"Invalid output size: {v} - expected 256 or 512 pixel image size")
        return v

    @model_validator(mode="after")
    def validate_inference_steps(self):
        if self.model == "tinysd" and self.num_inference_steps > 2000:
            raise ValueError(f"TinySD model cannot have more than 2000 inference steps")
        return self


class ModelResponse(BaseModel):
    request_id: Annotated[str, Field(default_factory=lambda: uuid4().hex)]
    ip: Annotated[str, IPvAnyAddress] | None
    content: Annotated[str | bytes, Field(min=0, max=10000)]
    created_at: datetime = datetime.now()


class TextModelResponse(ModelResponse):
    price: Annotated[float, Field(gte=0, default=0.01)]

    @computed_field
    @property
    def tokens(self) -> int:
        return count_tokens(self.content)

    @computed_field
    @property
    def cost(self) -> float:
        return self.price * self.tokens


class ImageModelResponse(ModelResponse):
    size: tuple[int, int] = tuple[Field(gte=0), Field(gte=0)]
    url: Annotated[str, HttpUrl] | None = None
