from typing import Dict, Optional
from enum import Enum

from pydantic import BaseModel, Field

from fastapi import FastAPI, Body, Path, Query

app: FastAPI = FastAPI(
    title="Person API"
)

# Models


class HairColor(Enum):
    white = "white"
    brown = "brown"
    black = "black"
    blonde = "blonde"
    red = "red"


class Person(BaseModel):
    first_name: str = Field(..., min_length=3, max_length=20, title="Person first name",
                            description="This is the person first name. It's required!")
    last_name: str = Field(..., min_length=3, max_length=20, title="Person last name",
                           description="This is the person last name. It's required!")
    age: int = Field(..., gt=0, title="Person age",
                     description="This is the person age")
    hair_color: Optional[HairColor] = Field(
        default=None, title="Person hair color")
    is_married: Optional[bool] = Field(default=None)


class Address(BaseModel):
    city: str
    state: str
    country: str


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


@app.put("/person/{person_id}")
def update_person(
    person_id: int = Path(
        ...,
        title="Person ID",
        description="This is the person ID",
        gt=0
    ),
    person: Person = Body(...),
    address: Address = Body(...)
) -> Dict:
    results = person.dict()
    results.update(address.dict())

    return results
