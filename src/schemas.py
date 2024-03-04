from dataclasses import dataclass
from typing import Literal


@dataclass
class TextModelRequest:
    model: Literal["tinyllama", "gemma2b"]
    prompt: str
    temperature: float


@dataclass
class TextModelResponse:
    tokens: int
    response: str
