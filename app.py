from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import subprocess
import uuid
import os
import yaml

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # atau spesifik: ["http://localhost:3000"]
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

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
    uuid_spec = uuid.uuid4();
    foldername = f"/output/{uuid_spec}"
    
    os.makedirs(foldername, exist_ok=True)
    filename = f"{foldername}/request.yaml"

    # yaml_str = yaml.dump(data.yaml, sort_keys=False)

    with open(filename, "w") as f:
        f.write(data.yaml)

    result = subprocess.run(
        ["rendercv", "render", filename],
        check=True,
        capture_output=True,
        text=True
    )

    if result.returncode != 0:
        return {
            "status": "error",
            "stderr": result.stderr
        }

    return {
        "status": "ok",
        "stdout": result.stdout
    }
