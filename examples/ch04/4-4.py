# utils.py

from dataclasses import dataclass
from typing import Literal, TypeAlias
from utils import count_tokens

SupportedModels: TypeAlias = Literal["gpt-3.5", "gpt-4"]
PriceTable: TypeAlias = dict[SupportedModels, float]
prices: PriceTable = {"gpt-3.5": 0.0030, "gpt-4": 0.0200}


@dataclass
class Message:
    prompt: str
    response: str | None
    model: SupportedModels


@dataclass
class MessageCostReport:
    req_costs: float
    res_costs: float
    total_costs: float


# Define count_tokens function as normal
...


def calculate_usage_costs(message: Message) -> MessageCostReport:
    if message.model not in prices:
        # raise at runtime - in case someone ignores type errors
        raise ValueError(
            f"Cost calculation is not supported for {message.model} model."
        )
    price = prices[message.model]
    req_costs = price * count_tokens(message.prompt) / 1000
    res_costs = price * count_tokens(message.response) / 1000
    total_costs = req_costs + res_costs
    return MessageCostReport(
        req_costs=req_costs, res_costs=res_costs, total_costs=total_costs
    )
