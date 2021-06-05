import shutil
from tempfile import NamedTemporaryFile

import streamlit as st
from PIL import Image

from seamless_image_gen import seamless_image_gen


def tile_image(image, num):
    dst = Image.new("RGB", (image.width * num, image.height * num))
    for w in range(num):
        for h in range(num):
            dst.paste(image, (image.width * w, image.height * h))

    return dst


image_sizes = ["128x128", "256x256", "512x512"]

st.title("Seamless Image Generator")


uploaded_file = st.file_uploader("Choose an image...", type=["png", "jpg"])
if uploaded_file is not None:
    with NamedTemporaryFile() as fin, NamedTemporaryFile(suffix=".png") as fout:
        shutil.copyfileobj(uploaded_file, fin)
        image = Image.open(uploaded_file).convert("RGB")
        left_column, right_column = st.beta_columns(2)
        left_column.header("Uploaded Image")
        left_column.image(image)
        right_column.header("Generate Image Size")
        image_size_str = right_column.radio("image size", ["-"] + image_sizes)
        if image_size_str in image_sizes:
            image_size = int(image_size_str.split("x")[0])
            st.header("Original")
            left_column, right_column = st.beta_columns([1, 2])
            resized_image = image.resize((image_size, image_size))
            left_column.image(
                resized_image, caption=image_size_str, use_column_width=True
            )
            right_column.image(
                tile_image(resized_image, 3),
                caption="tiled",
                use_column_width=True,
            )

            st.header("Generated")
            left_column, right_column = st.beta_columns([1, 2])
            seamless_image_gen(
                fin.name,
                fout.name,
                image_size=image_size,
                fill_width=0.1,
                fill_height=0.1,
            )
            image = Image.open(fout.name)
            left_column.image(image, caption=image_size_str, use_column_width=True)
            right_column.image(
                tile_image(image, 3),
                caption="tiled",
                use_column_width=True,
            )
