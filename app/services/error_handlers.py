from fastapi import FastAPI
from app.services.errors import ETLError, etl_error_handler

def register_exception_handlers(app: FastAPI) -> None:
    """Registra los manejadores de excepciones globales en la aplicación FastAPI."""
    app.add_exception_handler(ETLError, etl_error_handler) #type: ignore