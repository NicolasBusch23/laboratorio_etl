from fastapi import APIRouter, status
from app.services.etl_service import extract_games_to_mongo
from app.services.etl_service import transform_and_load_games_to_mysql
from app.services.etl_service import reset_etl_storage
from app.views.schemas import ExtractRequest
from app.views.schemas import ResetResponse


#----Versión 1 de la API - ETL Juegos----#
router = APIRouter(prefix="/api/v1/etl", tags=["ETL Juegos v1"])

@router.post("/extraer", status_code=status.HTTP_201_CREATED)
def extract(request: ExtractRequest):
    """
    Ejecuta el paso EXTRACT del proceso ETL.

    - Consume la API pública de juegos.
    - Extrae una cantidad definida de registros.
    - Almacena los datos crudos (RAW) en MongoDB.
    - Garantiza idempotencia usando el ID del juego como clave primaria.

    Retorna un mensaje de cuántos registros fueron guardados y si fue exitosa la solicitud.
    """
    result = extract_games_to_mongo(request.cantidad)
    return result

@router.post("/transformar", status_code=status.HTTP_200_OK)
def transformar():
    return transform_and_load_games_to_mysql()

from app.services.etl_service import reset_etl_storage
from app.views.schemas import ResetResponse

@router.delete("/reset", status_code=status.HTTP_200_OK, response_model=ResetResponse)
def reset():
    return reset_etl_storage()
