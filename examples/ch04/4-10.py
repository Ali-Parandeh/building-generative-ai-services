# schemas.py

from typing import Annotated
from pydantic import computed_field, Field
from utils import count_tokens

...


class TextModelResponse(ModelResponse):
    price: Annotated[float, Field(ge=0, default=0.01)]

    @computed_field
    @property
    def tokens(self) -> int:
        return count_tokens(self.content)

    @computed_field
    @property
    def cost(self) -> float:
        return self.price * self.tokens
