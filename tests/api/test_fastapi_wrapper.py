from http import HTTPStatus
from typing import Optional

from fastapi import HTTPException

from fastapi.testclient import TestClient

from regtech_api_commons.api.exceptions import RegTechHttpException
from regtech_api_commons.api.fastapi_wrapper import RegtechApp
from pydantic import BaseModel, Field

app = RegtechApp()


class GreetingResponse(BaseModel):
    greeting: str = Field(pattern=r"^[a-zA-Z,! ]+$")


@app.get("/hello/{name}")
def say_hi(name: str, age: Optional[int] = None) -> GreetingResponse:
    if age and age > 120:
        raise RegTechHttpException(status_code=HTTPStatus.UNPROCESSABLE_ENTITY, detail="age is too high")
    if name == "foo":
        raise HTTPException(status_code=HTTPStatus.FORBIDDEN, detail="Foo is not a person")
    return {
        "greeting": f"Hello, {name}!",
    }


client = TestClient(app)


def test_hello():
    response = client.get("/hello/Bob")
    assert response.status_code == 200, response.text
    assert response.json() == {"greeting": "Hello, Bob!"}


def test_hello_regtech_exception_error():
    response = client.get("/hello/Bob?age=130")
    assert response.status_code == 422, response.text
    assert response.json() == {
        'error_detail': 'age is too high',
        'error_name': None,
    }


def test_hello_request_validation_error():
    response = client.get("/hello/bob?age=foo")
    assert response.status_code == 422, response.text
    assert response.json() == {
        "error_detail": "[{'type': 'int_parsing', 'loc': ('query', 'age'), 'msg': 'Input should be a valid integer, "
                        "unable to parse string as an integer', 'input': 'foo'}]",
        "error_name": "Request Validation Failure",
    }


def test_hello_response_validation_error():
    response = client.get("/hello/Joe1")
    assert response.status_code == 500, response.text
    assert response.json() == {
        'error_detail': '["String should match pattern \'^[a-zA-Z,! ]+$\'"]',
        'error_name': 'Response Validation Failure',
    }


def test_hello_http_exception():
    response = client.get("/hello/foo")
    assert response.status_code == 403, response.text
    assert response.json() == {
        'error_detail': 'Foo is not a person',
        'error_name': 'Forbidden',
    }
