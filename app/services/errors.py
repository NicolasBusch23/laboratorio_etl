from fastapi import Request, status
from fastapi.responses import JSONResponse

class ETLError(Exception):
    status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
    detail = "Error interno del ETL"

    def __init__(self, detail: str | None = None):
        if detail:
            self.detail = detail

class InvalidCantidadError(ETLError):
    status_code = status.HTTP_400_BAD_REQUEST
    detail = "La cantidad debe ser mayor que 0"

class EmptyStagingError(ETLError):
    status_code = status.HTTP_404_NOT_FOUND
    detail = "No hay datos en MongoDB para transformar"

class ExternalAPIError(ETLError):
    status_code = status.HTTP_502_BAD_GATEWAY
    detail = "Error consumiendo la API externa"

class MongoError(ETLError):
    status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
    detail = "Error accediendo a MongoDB"

class MySQLError(ETLError):
    status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
    detail = "Error accediendo a MySQL"

async def etl_error_handler(request: Request, exc: ETLError):
    return JSONResponse(
        status_code=exc.status_code,
        content={"mensaje": exc.detail, "status": exc.status_code},
    )
