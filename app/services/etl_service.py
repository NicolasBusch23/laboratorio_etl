import logging
from typing import Dict, List
import requests

from app.database import mongo_collection

log = logging.getLogger(__name__)

FREE_TO_GAME_URL = "https://www.freetogame.com/api/games"

def _fetch_games_list(base_url: str) -> List[Dict]:
    resp = requests.get(base_url, timeout=30)
    resp.raise_for_status()
    return resp.json()  # lista completa

def extract_games_to_mongo(cantidad: int) -> dict:
    """
    EXTRACT: Consume la API y guarda 'cantidad' registros en MongoDB con idempotencia.
    """

    if cantidad <= 0:
        raise ValueError("La cantidad debe ser mayor que 0")

    log.info("Starting EXTRACT: requesting %d games", cantidad)

    games = _fetch_games_list(FREE_TO_GAME_URL)

    # Tomar solo la cantidad solicitada
    games = games[:cantidad]

    guardados = 0

    for game in games:
        try:
            # Idempotencia: usar id como clave natural
            mongo_collection.replace_one(
                {"id": game.get("id")},
                game,
                upsert=True
            )
            guardados += 1
        except Exception as exc:
            log.warning("Failed to upsert game %s: %s", game.get("title"), exc)

    return {
        "mensaje": "Datos extraídos exitosamente",
        "registros_guardados": guardados,
        "fuente": "FreeToGame API",
        "status": 201
    }