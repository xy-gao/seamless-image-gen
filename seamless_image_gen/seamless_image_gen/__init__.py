import os
from tempfile import NamedTemporaryFile

from generative_inpainting import GenerativeInpainter

from .image_generator import (
    CenterCrossMaskImageGenerator,
    CenterOfTileImageGenerator,
    CV2IdenticalImageGenerator,
    ResizedImageGenerator,
)


def tmp_png():
    return NamedTemporaryFile(suffix=".png")


def seamless_image_gen(
    input_path: str,
    output_path: str,
    image_size: int = 512,
    fill_width: float = 0.1,
    fill_height: float = 0.1,
):
    with tmp_png() as tmp1, tmp_png() as tmp2, tmp_png() as tmp3, tmp_png() as tmp4:
        ResizedImageGenerator(width=image_size, height=image_size)(
            input_path, tmp1.name
        )
        CenterOfTileImageGenerator()(tmp1.name, tmp2.name)
        CenterCrossMaskImageGenerator(width=fill_width, height=fill_height)(
            tmp2.name, tmp3.name
        )
        GenerativeInpainter(os.environ["CHECKPOINTS_PATH"])(
            tmp2.name, tmp3.name, tmp4.name, image_size=[image_size, image_size]
        )
        CenterOfTileImageGenerator()(tmp4.name, output_path)
