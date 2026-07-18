from fastapi import Request


def get_constraint_registry(
    request: Request,
):
    return request.app.state.registry