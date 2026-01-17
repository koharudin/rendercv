from fastapi import FastAPI
from pydantic import BaseModel
import subprocess
import uuid
import os

app = FastAPI()

class CVRequest(BaseModel):
    yaml: str

@app.get("/")
def homepage():
    return {
        "status":"ok",
        "message":"rendercv webservice"
    }

@app.post("/render")
def render_cv(data: CVRequest):
    filename = f"/output/{uuid.uuid4()}.yaml"
    output_dir = "/output"

    with open(filename, "w") as f:
        f.write(data.yaml)

    subprocess.run(
        ["rendercv", "render", filename],
        check=True
    )

    return {
        "status": "ok ",
        "files": os.listdir(output_dir)
    }
