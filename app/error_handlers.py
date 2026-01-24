from fastapi import FastAPI
from fastapi.responses import JSONResponse

from .services.errors import PersonaNotFoundError, EmailAlreadyExistsError


def register_exception_handlers(app: FastAPI) -> None:
    """Register global exception handlers mapping domain errors to HTTP responses."""

    @app.exception_handler(PersonaNotFoundError)
    def _handle_not_found(_: object, __: PersonaNotFoundError):
        return JSONResponse(status_code=404, content={"detail": "Persona not found"})

    @app.exception_handler(EmailAlreadyExistsError)
    def _handle_conflict(_: object, __: EmailAlreadyExistsError):
        return JSONResponse(status_code=409, content={"detail": "Email already registered"})
