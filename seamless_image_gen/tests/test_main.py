import os

from seamless_image_gen import seamless_image_gen


def abs_path(file_path):
    return os.path.join(os.path.dirname(os.path.abspath(__file__)), file_path)


def test_seamless_image_gen():
    input_file = "test_imgs/original.png"
    actual_file = "test_imgs/actual.png"
    input_path = abs_path(input_file)
    actual_path = abs_path(actual_file)
    seamless_image_gen(input_path, actual_path)
    if os.path.exists(actual_path):
        os.remove(actual_path)
        file_exist = True
    else:
        file_exist = False
    assert file_exist
