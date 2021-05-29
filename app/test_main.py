import os
from shutil import copyfile

import pytest
from fastapi.testclient import TestClient

from main import app

client = TestClient(app)


def mock_seamless_image_gen(src, dst, *args, **kwargs):
    copyfile(src, dst)


def test_inpaint(monkeypatch):
    monkeypatch.setattr("main.seamless_image_gen", mock_seamless_image_gen)
    image_path = os.path.join(
        os.path.dirname(os.path.abspath(__file__)),
        "../seamless_image_gen/tests/test_imgs/original.png",
    )
    with open(image_path, "rb") as img:
        response = client.post(
            "/inpaint/?size=512&width=0.1&height=0.1", files={"file": img}
        )
    assert response.status_code == 200
    assert response.headers["Content-Type"] == "image/png"


@pytest.mark.parametrize(
    "size, width, height",
    [(100, 0.1, 0.1), (512, 1.1, 0.1), (512, 0.1, 1.1)],
)
def test_inpaint_parameters_not_allowed(monkeypatch, size, width, height):
    monkeypatch.setattr("main.seamless_image_gen", mock_seamless_image_gen)

    image_path = os.path.join(
        os.path.dirname(os.path.abspath(__file__)),
        "../seamless_image_gen/tests/test_imgs/original.png",
    )
    with open(image_path, "rb") as img:
        response = client.post(
            f"/inpaint/?size={size}&width={width}&height={height}", files={"file": img}
        )
    assert response.status_code == 422
