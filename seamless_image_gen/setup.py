from setuptools import setup

setup(
    name="seamless_image_gen",
    version="0.0.0",
    author="Xiangyi Gao",
    description="generate seamless image from original image",
    packages=["seamless_image_gen"],
    install_requires=[
        "opencv-python==4.5.2.52",
        "numpy==1.19.5",
        "generative_inpainting @ git+https://git@github.com/xy-gao/generative-inpainting-pytorch@master#egg=generative-inpainting-pytorch&subdirectory=generative_inpainting",
    ],
    extras_require={"dev": ["pytest"]},
)
