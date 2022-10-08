from typing import Dict
from fastapi import FastAPI

app: FastAPI = FastAPI()


@app.get("/")
def home() -> Dict:
    return {
        "body": "Hello World"
    }
