from datetime import datetime
from typing import Annotated, Literal
from uuid import uuid4

from pydantic import BaseModel, Field, HttpUrl, IPvAnyAddress, PositiveInt, computed_field

from utils import count_tokens


class ModelRequest(BaseModel):
    prompt: Annotated[str, Field(min=1, max=4000)]


class TextModelRequest(ModelRequest):
    model: Literal["tinyllama", "gemma2b"]
    temperature: Annotated[float, Field(gt=0.0, lte=1.0, default=0.01)]


class ImageModelRequest(ModelRequest):
    model: Literal["tinysd", "dalle"]
    output_size: tuple[PositiveInt, PositiveInt]
    num_inference_steps: PositiveInt = 200


class ModelResponse(BaseModel):
    request_id: Annotated[str, Field(default_factory=lambda: uuid4().hex)]
    ip: Annotated[str, IPvAnyAddress]
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
    url: HttpUrl | None = None
