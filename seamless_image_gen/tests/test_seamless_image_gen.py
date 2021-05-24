import os

from seamless_image_gen import CenterOfTileImageGenerator, CV2IdenticalImageGenerator


def file_exist(path):
    if os.path.exists(path):
        os.remove(path)
        return True
    else:
        return False


def test_cv2_identical_image_generator():
    input_path = os.path.join(
        os.path.dirname(os.path.abspath(__file__)), "test_imgs/1.jpg"
    )
    output_path = os.path.join(
        os.path.dirname(os.path.abspath(__file__)), "test_imgs/out_1.jpg"
    )
    CV2IdenticalImageGenerator()(input_path, output_path)
    assert file_exist(output_path)


def test_center_of_tile_image_generator():
    input_path = os.path.join(
        os.path.dirname(os.path.abspath(__file__)), "test_imgs/1.jpg"
    )
    output_path = os.path.join(
        os.path.dirname(os.path.abspath(__file__)), "test_imgs/out_1.jpg"
    )
    CenterOfTileImageGenerator()(input_path, output_path)
    assert file_exist(output_path)
