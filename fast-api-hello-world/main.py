from typing import Dict, Optional

from pydantic import BaseModel

from fastapi import FastAPI, Body, Path, Query

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


@app.get("/person/detail")
def show_person(
    name: Optional[str] = Query(
        None,
        min_length=3,
        max_length=20,
        title="Person name",
        description="This is the person name"
    ),
    age: Optional[int] = Query(
        ...,
        gt=0,
        lt=100,
        title="Person age",
        description="This is the person age. It's required"
    )
) -> Dict:
    return {
        "name": name,
        "age": age
    }


@app.get("person/detail/{person_id}")
def show_person(
    person_id: int = Path(..., gt=0)
) -> Dict:
    return {
        "person_id": person_id
    }
