from fastapi import APIRouter, status
from app.services.etl_service import extract_games_to_mongo
from app.views.schemas import ExtractRequest

router = APIRouter(prefix="/etl juegos", tags=["ETL Juegos"])

@router.post("/extract", status_code=status.HTTP_201_CREATED)
def extract(request: ExtractRequest):
    """
    Paso EXTRACT: API -> MongoDB (RAW)
    """
    result = extract_games_to_mongo(request.cantidad)
    return result