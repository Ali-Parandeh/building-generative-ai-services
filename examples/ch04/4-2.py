# utils.py

from typing import Literal, TypeAlias
from loguru import logger
import tiktoken


SupportedModels: TypeAlias = Literal["gpt-3.5", "gpt-4"]
PriceTable: TypeAlias = dict[SupportedModels, float]
price_table: PriceTable = {"gpt-3.5": 0.0030, "gpt-4": 0.0200}


def count_tokens(text: str | None) -> int:
    if text is None:
        logger.warning("Response is None. Assuming 0 tokens used")
        return 0
    enc = tiktoken.encoding_for_model("gpt-4o")
    return len(enc.encode(text))


def calculate_usage_costs(
    prompt: str,
    response: str | None,
    model: SupportedModels,
) -> tuple[float, float, float]:
    if model not in price_table:
        # raise at runtime - in case someone ignores type errors
        raise ValueError(f"Cost calculation is not supported for {model} model.")
    price = price_table[model]
    req_costs = price * count_tokens(prompt) / 1000
    res_costs = price * count_tokens(response) / 1000
    total_costs = req_costs + res_costs
    return req_costs, res_costs, total_costs
