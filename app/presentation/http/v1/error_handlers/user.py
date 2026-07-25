from starlette import status
from starlette.responses import JSONResponse


def domain_invalid_data_error_handler(
    _,
    exception,
):
    return JSONResponse(
        status_code=status.HTTP_400_BAD_REQUEST,
        content={"detail": str(exception)},
    )