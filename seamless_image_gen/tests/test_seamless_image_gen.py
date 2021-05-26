import filecmp
import os

import pytest
from seamless_image_gen import (
    CenterCrossMaskImageGenerator,
    CenterOfTileImageGenerator,
    CV2IdenticalImageGenerator,
)


def files_equal(acutal_path, expected_path):
    if os.path.exists(acutal_path):
        is_equal = filecmp.cmp(acutal_path, expected_path, shallow=False)
        print(is_equal)
        os.remove(acutal_path)
        return is_equal
    else:
        return False


def abs_path(file_path):
    return os.path.join(os.path.dirname(os.path.abspath(__file__)), file_path)


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
    ],
)
def test_image_generator(image_generator, input_file, actual_file, expected_file):
    input_path = abs_path(input_file)
    actual_path = abs_path(actual_file)
    expected_path = abs_path(expected_file)
    image_generator(input_path, actual_path)
    assert files_equal(actual_path, expected_path)
