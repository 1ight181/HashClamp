from fastapi import FastAPI

from shared.exceptions.not_found import EntityNotFoundError
from app.presentation.http.v1.error_handlers.not_found import entity_not_found_handler


def register_exception_handlers(app: FastAPI):
    app.add_exception_handler(
        EntityNotFoundError,
        entity_not_found_handler,
    )