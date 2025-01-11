# utils.py
import os
import tempfile
from io import BytesIO
from pathlib import Path

import open3d as o3d
import torch
from diffusers.pipelines.shap_e.renderer import MeshDecoderOutput


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
