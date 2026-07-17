from fastapi import Request

from app.infrastructure.persistence.sqlalchemy.db import Database


def get_database(
    request: Request,
) -> Database:

    return request.app.state.database
