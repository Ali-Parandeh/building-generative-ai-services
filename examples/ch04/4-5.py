from typing import Literal
from pydantic import BaseModel


class TextModelRequest(BaseModel):
    model: Literal["gpt-3.5-turbo", "gpt-4o"]
    prompt: str
    temperature: float = 0.0
