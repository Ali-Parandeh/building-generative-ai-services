from typing import Literal
from pydantic import BaseModel


class TextModelRequest(BaseModel):
    model: Literal["tinyllama", "gemma2b"]
    prompt: str
    temperature: float = 0.0
