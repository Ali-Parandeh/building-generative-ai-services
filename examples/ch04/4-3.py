from typing import Annotated, Literal

SupportedModelType = Annotated[Literal["gpt-3.5-turbo", "gpt-4o"], "Supported models"]
PriceTableType = Annotated[dict[SupportedModelType, float], "Supported model pricing table"]


prices: PriceTableType = {
    "gpt-4o": 0.000638,
    "gpt4-o": 0.000638,
    # error: Dict entry 1 has incompatible type "Literal['gpt4-o']" [dict-item]
    "gpt-4": 0.000638,
}
# error: Dict entry 2 has incompatible type "Literal['gpt-4']" [dict-item]
