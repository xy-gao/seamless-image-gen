import os
import shutil
from tempfile import NamedTemporaryFile

from fastapi import BackgroundTasks, FastAPI, File, HTTPException, Query, UploadFile
from fastapi.responses import FileResponse
from seamless_image_gen import seamless_image_gen

app = FastAPI()


def remove_file(path):
    os.remove(path)


@app.post("/inpaint")
def inpaint(
    background_tasks: BackgroundTasks,
    size: int = 512,
    width: float = Query(0.1, ge=0, le=1),
    height: float = Query(0.1, ge=0, le=1),
    file: UploadFile = File(...),
):
    if size not in [128, 256, 512]:
        raise HTTPException(
            status_code=422, detail="size not allowed, choose from 128, 256, 512"
        )
    with NamedTemporaryFile(suffix=".png") as fin, NamedTemporaryFile(
        suffix=".png", delete=False
    ) as fout:
        shutil.copyfileobj(file.file, fin)
        seamless_image_gen(
            fin.name, fout.name, image_size=size, fill_width=width, fill_height=height
        )
    background_tasks.add_task(remove_file, fout.name)
    return FileResponse(fout.name, media_type="image/png")
