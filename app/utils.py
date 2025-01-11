from io import BytesIO
import soundfile
import numpy as np
import av
import os
import tempfile
from pathlib import Path

import open3d as o3d
import torch
from diffusers.pipelines.shap_e.renderer import MeshDecoderOutput


def audio_array_to_buffer(audio_array: np.array, sample_rate: int) -> BytesIO:
    buffer = BytesIO()
    soundfile.write(buffer, audio_array, sample_rate, format="wav")
    buffer.seek(0)
    return buffer


from typing import Literal

from PIL import Image
from io import BytesIO


def img_to_bytes(
    image: Image.Image, img_format: Literal["PNG", "JPEG"] = "PNG"
) -> bytes:
    buffer = BytesIO()
    image.save(buffer, format=img_format)
    return buffer.getvalue()


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
        packet = stream.encode(frame)
        output.mux(packet)
    packet = stream.encode(None)
    output.mux(packet)
    return buffer


def mesh_to_obj_buffer(mesh: MeshDecoderOutput) -> BytesIO:
    mesh_o3d = o3d.geometry.TriangleMesh()
    mesh_o3d.vertices = o3d.utility.Vector3dVector(
        mesh.verts.cpu().detach().numpy()
    )
    mesh_o3d.triangles = o3d.utility.Vector3iVector(
        mesh.faces.cpu().detach().numpy()
    )

    if len(mesh.vertex_channels) == 3:  # You have color channels
        vert_color = torch.stack(
            [mesh.vertex_channels[channel] for channel in "RGB"], dim=1
        )
        mesh_o3d.vertex_colors = o3d.utility.Vector3dVector(
            vert_color.cpu().detach().numpy()
        )

    with tempfile.NamedTemporaryFile(delete=False, suffix=".obj") as tmp:
        o3d.io.write_triangle_mesh(Path(tmp.name), mesh_o3d, write_ascii=True)
        with open(tmp.name, "rb") as f:
            buffer = BytesIO(f.read())
        os.remove(tmp.name)

    return buffer
