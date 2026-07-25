from fastapi import FastAPI

from app.application.exceptions.not_found import EntityNotFoundError
from app.domain.entities.exceptions import DomainInvalidDataError
from app.presentation.http.v1.error_handlers.not_found import entity_not_found_handler
from app.presentation.http.v1.error_handlers.user import domain_invalid_data_error_handler


def register_exception_handlers(app: FastAPI):
    app.add_exception_handler(
        EntityNotFoundError,
        entity_not_found_handler,
    )

    app.add_exception_handler(
        DomainInvalidDataError,
        domain_invalid_data_error_handler,
    )