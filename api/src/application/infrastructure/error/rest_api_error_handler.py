from application.infrastructure.error.errors import HousingUnitBaseError
from starlette.responses import JSONResponse
from fastapi import FastAPI, Request


def initialize_rest_api_error_handlers(rest_api: FastAPI) -> None:
    @rest_api.exception_handler(HousingUnitBaseError)
    async def unicorn_exception_handler(request: Request, exc: HousingUnitBaseError):
        return JSONResponse(
            status_code=400,
            content={
                "Detail": "{}".format(exc.args[0]),
                "Type": "{}".format(exc.error_type)
            },
        )
