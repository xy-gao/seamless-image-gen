import filecmp
import os

import pytest
from seamless_image_gen import (
    CenterCrossMaskImageGenerator,
    CenterOfTileImageGenerator,
    CV2IdenticalImageGenerator,
    ResizedImageGenerator,
)

from .test_main import abs_path


def files_equal(actual_path, expected_path):
    if os.path.exists(actual_path):
        is_equal = filecmp.cmp(actual_path, expected_path, shallow=False)
        print(is_equal)
        os.remove(actual_path)
        return is_equal
    else:
        return False


@pytest.mark.parametrize(
    "image_generator, input_file, actual_file, expected_file",
    [
        (
            CV2IdenticalImageGenerator(),
            "test_imgs/original.png",
            "test_imgs/actual_1.png",
            "test_imgs/expected_1.png",
        ),
        (
            CenterOfTileImageGenerator(),
            "test_imgs/original.png",
            "test_imgs/actual_2.png",
            "test_imgs/expected_2.png",
        ),
        (
            CenterCrossMaskImageGenerator(),
            "test_imgs/original.png",
            "test_imgs/actual_3.png",
            "test_imgs/expected_3.png",
        ),
        (
            ResizedImageGenerator(),
            "test_imgs/original.png",
            "test_imgs/actual_4.png",
            "test_imgs/expected_4.png",
        ),
    ],
)
def test_image_generator(image_generator, input_file, actual_file, expected_file):
    input_path = abs_path(input_file)
    actual_path = abs_path(actual_file)
    expected_path = abs_path(expected_file)
    image_generator(input_path, actual_path)
    assert files_equal(actual_path, expected_path)


def test_center_ratio_out_of_range():
    with pytest.raises(ValueError) as e:
        CenterCrossMaskImageGenerator(width=1.1, height=1.3)
    assert str(e.value) == "ratio out of range"
