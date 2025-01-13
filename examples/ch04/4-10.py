# schemas.py

from typing import Annotated
from pydantic import computed_field, Field
from utils import count_tokens

...


class TextModelResponse(ModelResponse):
    model: SupportedModels
    price: Annotated[float, Field(ge=0, default=0.01)]
    temperature: Annotated[float, Field(ge=0.0, le=1.0, default=0.0)]

    @property
    @computed_field
    def tokens(self) -> int:
        return count_tokens(self.content)

    @property
    @computed_field
    def cost(self) -> float:
        return self.price * self.tokens
