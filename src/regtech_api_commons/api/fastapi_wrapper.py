from fastapi import FastAPI
from fastapi.exceptions import RequestValidationError, ResponseValidationError
from starlette.exceptions import HTTPException
from regtech_api_commons.api.exceptions import RegTechHttpException
from regtech_api_commons.api.exception_handlers import (
    http_exception_handler,
    general_exception_handler,
    regtech_http_exception_handler,
    request_validation_error_handler,
    response_validation_error_handler,
)
from pydantic import ValidationError


class RegtechApp(FastAPI):
    """
    FastAPI subclass that automatically attaches some standard Regtech error handlers.  It can also be used to perform
    additional common configuration/behvaior if necessary.
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.add_exception_handler(RegTechHttpException, regtech_http_exception_handler)  # type: ignore[type-arg]  # noqa: E501
        self.add_exception_handler(RequestValidationError, request_validation_error_handler)  # type: ignore[type-arg]  # noqa: E501
        self.add_exception_handler(HTTPException, http_exception_handler)  # type: ignore[type-arg]  # noqa: E501
        self.add_exception_handler(ResponseValidationError, response_validation_error_handler)  # type: ignore[type-arg]  # noqa: E5010
        self.add_exception_handler(ValidationError, response_validation_error_handler)  # type: ignore[type-arg]  # noqa: E5010
        self.add_exception_handler(Exception, general_exception_handler)  # type: ignore[type-arg]  # noqa: E501
