# schemas.py

from typing import Annotated, Literal

from pydantic import (
    AfterValidator,
    BaseModel,
    Field,
    PositiveInt,
    validate_call,
)

ImageSize = Annotated[
    tuple[PositiveInt, PositiveInt], "Width and height of an image in pixels"
]
SupportedModels = Annotated[
    Literal["tinysd", "sd1.5"], "Supported Image Generation Models"
]


@validate_call
def is_square_image(value: ImageSize) -> ImageSize:
    if value[0] / value[1] != 1:
        raise ValueError("Only square images are supported")
    if value[0] not in [512, 1024]:
        raise ValueError(f"Invalid output size: {value} - expected 512 or 1024")
    return value


@validate_call
def is_valid_inference_step(
    num_inference_steps: int, model: SupportedModels
) -> int:
    if model == "tinysd" and num_inference_steps > 2000:
        raise ValueError(
            "TinySD model cannot have more than 2000 inference steps"
        )
    return num_inference_steps


OutputSize = Annotated[ImageSize, AfterValidator(is_square_image)]
InferenceSteps = Annotated[
    int,
    AfterValidator(
        lambda v, values: is_valid_inference_step(v, values["model"])
    ),
]


class ModelRequest(BaseModel):
    prompt: Annotated[str, Field(min_length=1, max_length=4000)]


class ImageModelRequest(ModelRequest):
    model: SupportedModels
    output_size: OutputSize
    num_inference_steps: InferenceSteps = 200
