from fastapi import FastAPI
from fastapi import UploadFile
from fastapi import File

from fastapi.middleware.cors import CORSMiddleware

import tempfile

from app.graph.ingredient_graph import graph

app = FastAPI(
    title="Ladder API",
    version="0.1.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/health")
def health():
    return {
        "status": "ok"
    }


@app.post("/ingredients/image")
async def ingredient_image(
    file: UploadFile = File(...)
):

    temp = tempfile.NamedTemporaryFile(
        delete=False,
        suffix=".jpg"
    )

    temp.write(
        await file.read()
    )

    result = graph.invoke(
        {
            "image_path": temp.name,
            "ingredients": []
        }
    )

    return result