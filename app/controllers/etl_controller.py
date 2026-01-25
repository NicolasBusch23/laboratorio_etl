from fastapi import APIRouter, status
from app.services.etl_service import extract_games_to_mongo
from app.views.schemas import ExtractRequest

router = APIRouter(prefix="/etl", tags=["ETL Juegos"])

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