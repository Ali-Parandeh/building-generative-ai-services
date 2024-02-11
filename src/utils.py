from io import BytesIO
from typing import Literal

from PIL import Image


def img_to_bytes(image: Image.Image, img_format: Literal["PNG", "JPEG"] = "PNG") -> BytesIO:
    img_bytes = BytesIO()
    image.save(img_bytes, format=img_format)
    img_bytes.seek(0)
    return img_bytes
