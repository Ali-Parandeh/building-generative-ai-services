from io import BytesIO
from typing import Literal

import tiktoken
from loguru import logger
from PIL import Image

SupportedModelType = Literal["gpt-3.5", "gpt-4"]
PriceTableType = dict[SupportedModelType, float]

price_table: PriceTableType = {"gpt-3.5": 0.0030, "gpt-4": 0.0200}


def count_tokens(text: str | None) -> int:
    if not isinstance(text, str | None):
        raise ValueError(
            "'count_tokens' function only allows strings or None types. "
            f"`text` parameter of type {type(text)} was passed in"
        )
    if text is None:
        logger.warning("Response is None. Assuming 0 tokens used")
        return 0
    enc = tiktoken.get_encoding("cl100k_base")
    return len(enc.encode(text))


def calculate_usage_costs(
    prompt: str, response: str | None, model: SupportedModelType, prices: PriceTableType
) -> tuple[float, float, float]:
    if model not in ["gpt-3.5", "gpt-4"]:
        # raise at runtime - in case someone ignores type errors
        raise ValueError(f"Cost calculation is not supported for {model} model.")
    try:
        price = prices[model]
    except KeyError as e:
        # raise at runtime - in case someone ignores type errors
        logger.warning(f"Pricing for model {model} is not available. " "Please update the pricing table.")
        raise e
    req_costs = price * count_tokens(prompt) / 1000
    res_costs = price * count_tokens(response) / 1000
    total_costs = req_costs + res_costs
    return req_costs, res_costs, total_costs


def img_to_bytes(image: Image.Image, img_format: Literal["PNG", "JPEG"] = "PNG") -> bytes:
    img_bytes = BytesIO()
    image.save(img_bytes, format=img_format)
    return img_bytes.getvalue()
