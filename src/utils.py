from io import BytesIO
from typing import Literal

import av
import numpy as np
import open3d as o3d
import soundfile
import tiktoken
import torch
from diffusers.pipelines.shap_e.renderer import MeshDecoderOutput
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
    prompt: str,
    response: str | None,
    model: SupportedModelType,
    prices: PriceTableType,
) -> tuple[float, float, float]:
    if model not in ["gpt-3.5", "gpt-4"]:
        # raise at runtime - in case someone ignores type errors
        raise ValueError(f"Cost calculation is not supported for {model} model.")
    try:
        price = prices[model]
    except KeyError as e:
        # raise at runtime - in case someone ignores type errors
        logger.warning(
            f"Pricing for model {model} is not available. " "Please update the pricing table."
        )
        raise e
    req_costs = price * count_tokens(prompt) / 1000
    res_costs = price * count_tokens(response) / 1000
    total_costs = req_costs + res_costs
    return req_costs, res_costs, total_costs


def img_to_bytes(image: Image.Image, img_format: Literal["PNG", "JPEG"] = "PNG") -> bytes:
    buffer = BytesIO()
    image.save(buffer, format=img_format)
    return buffer.getvalue()


def audio_array_to_buffer(audio_array: np.array, sample_rate: int) -> BytesIO:
    buffer = BytesIO()
    soundfile.write(buffer, audio_array, sample_rate, format="wav")
    buffer.seek(0)
    return buffer


def export_to_video_buffer(images: list[Image.Image]) -> BytesIO:
    buffer = BytesIO()
    output = av.open(buffer, "w", format="mp4")
    stream = output.add_stream("h264", 30)
    stream.width = images[0].width
    stream.height = images[0].height
    stream.pix_fmt = "yuv444p"
    stream.options = {"crf": "17"}
    for image in images:
        frame = av.VideoFrame.from_image(image)
        packet = stream.encode(frame)  # type: ignore
        output.mux(packet)
    packet = stream.encode(None)  # type: ignore
    output.mux(packet)
    return buffer


def mesh_to_ply_buffer(mesh: MeshDecoderOutput) -> BytesIO:
    buffer = BytesIO()
    mesh_o3d = o3d.geometry.TriangleMesh()
    mesh_o3d.vertices = o3d.utility.Vector3dVector(mesh.verts.cpu().detach().numpy())
    mesh_o3d.triangles = o3d.utility.Vector3iVector(mesh.faces.cpu().detach().numpy())

    if len(mesh.vertex_channels) == 3:  # You have color channels
        vert_color = torch.stack([mesh.vertex_channels[channel] for channel in "RGB"], dim=1)
        mesh_o3d.vertex_colors = o3d.utility.Vector3dVector(vert_color.cpu().detach().numpy())

    o3d.io.write_triangle_mesh(buffer, mesh_o3d, write_ascii=True, compressed=False)
    buffer.seek(0)
    return buffer
