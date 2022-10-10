from typing import Dict, Optional
from enum import Enum

from pydantic import BaseModel, EmailStr, Field

from fastapi import Cookie, FastAPI, Body, File, HTTPException, Header, Path, Query, UploadFile, status, Form

app: FastAPI = FastAPI(
    title="Person API"
)


class HairColor(Enum):
    white = "white"
    brown = "brown"
    black = "black"
    blonde = "blonde"
    red = "red"


class PersonBase(BaseModel):
    first_name: str = Field(
        ...,
        min_length=3,
        max_length=20,
        title="Person first name",
        description="This is the person first name. It's required!",
        example="Sergio"
    )
    last_name: str = Field(
        ...,
        min_length=3,
        max_length=20,
        title="Person last name",
        description="This is the person last name. It's required!",
        example="Aguirre Romero"
    )
    age: int = Field(
        ...,
        gt=0,
        title="Person age",
        description="This is the person age",
        example=26
    )
    hair_color: Optional[HairColor] = Field(
        default=None,
        title="Person hair color",
        example=HairColor.brown
    )
    is_married: Optional[bool] = Field(default=None)


class Person(PersonBase):
    password: str = Field(
        ...,
        min_length=8,
        title="Password",
        example="pass1234"
    )


class PersonResponse(PersonBase):
    pass


class Address(BaseModel):
    city: str
    state: str
    country: str

    class Config:
        schema_extra = {
            "example": {
                "city": "Medellin",
                "state": "Antioquia",
                "country": "Colombia"
            }
        }


class LoginResponse(BaseModel):
    username: str = Field(
        ...,
        max_length=20,
        example="zebek95"
    )


@app.get(
    path="/",
    status_code=status.HTTP_200_OK
)
def home() -> Dict:
    return {
        "body": "Hello World"
    }


@app.post(
    path="/person/new",
    response_model=PersonResponse,
    status_code=status.HTTP_201_CREATED
)
def create_person(person: Person = Body(...)) -> PersonResponse:
    return person


persons = [i for i in range(10)]


@app.get(
    path="/person/detail",
    status_code=status.HTTP_200_OK
)
def show_person(
    name: Optional[str] = Query(
        None,
        min_length=3,
        max_length=20,
        title="Person name",
        description="This is the person name",
        example="Sergio"
    ),
    age: Optional[int] = Query(
        ...,
        gt=0,
        lt=100,
        title="Person age",
        description="This is the person age. It's required",
        example=26
    )
) -> Dict:
    return {
        "name": name,
        "age": age
    }


@app.get(
    path="/person/detail/{person_id}",
    status_code=status.HTTP_200_OK,
)
def show_person(
    person_id: int = Path(
        ...,
        gt=0,
        example=1
    )
) -> Dict:
    if person_id not in persons:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="This person does not exist!"
        )

    return {
        "person_id": person_id
    }


@app.put(
    path="/person/{person_id}",
    status_code=status.HTTP_200_OK
)
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


@app.post(
    path="/login",
    response_model=LoginResponse,
    status_code=status.HTTP_200_OK
)
def login(
    username: str = Form(...),
    password: str = Form(...)
) -> LoginResponse:
    return LoginResponse(username=username)


@app.post(
    path="/contact",
    status_code=status.HTTP_200_OK
)
def contact(
    firts_name: str = Form(
        ...,
        max_length=20,
        min_length=4,
    ),
    last_name: str = Form(
        ...,
        max_length=20,
        min_length=4,
    ),
    email: EmailStr = Form(...),
    message: str = Form(
        ...,
        min_length=10
    ),
    user_agent: Optional[str] = Header(default=None),
    ads: Optional[str] = Cookie(default=None)
):
    return user_agent


@app.post(
    path="/upload-photo"
)
def upload_photo(
    image: UploadFile = File(...)
):
    return {
        "file_name": image.filename,
        "format": image.content_type,
        "size": len(image.file.read())
    }
