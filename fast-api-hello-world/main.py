from typing import Dict, Optional

from pydantic import BaseModel

from fastapi import FastAPI, Body

app: FastAPI = FastAPI()

# Models


class Person(BaseModel):
    first_name: str
    last_name: str
    age: int
    hair_color: Optional[str] = None
    is_married: Optional[bool] = None


@app.get("/")
def home() -> Dict:
    return {
        "body": "Hello World"
    }


@app.post("/person/new")
def create_person(person: Person = Body(...)) -> Person:
    return person
