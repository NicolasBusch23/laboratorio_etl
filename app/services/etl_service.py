import logging
from typing import Dict, List
import requests
import pandas as pd
from sqlalchemy.orm import Session
from app.database import mongo_collection, SessionLocal
from app.models.personajes_sql import Juego
from sqlalchemy import Date, inspect, text
from sqlalchemy.dialects import mysql


log = logging.getLogger(__name__)

FREE_TO_GAME_URL = "https://www.freetogame.com/api/games"

def _fetch_games_list(base_url: str) -> List[Dict]:
    resp = requests.get(base_url, timeout=30)
    resp.raise_for_status()
    return resp.json()  # lista completa

#---Extract
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


#---Transform & Load
def transform_and_load_games_to_mysql() -> dict:
    """
    Lee docs raw desde Mongo, transforma con Pandas y carga a MySQL (tabla juegos).
    Idempotente: si el ID ya existe, actualiza; si no existe, inserta.
    """
    # 1) Extract desde Mongo
    docs = list(mongo_collection.find({}))
    if not docs:
        return {
            "mensaje": "Pipeline finalizado",
            "registros_procesados": 0,
            "tabla_destino": Juego.__tablename__,
            "status": 200
        }

    # 2) Transform (aplanar + limpiar)
    df = pd.json_normalize(docs)  # aplana JSON a columnas [web:166]

    if "_id" in df.columns:
        df = df.drop(columns=["_id"])

    # Escogencia de columnas
    cols = [
        "id", "title", "thumbnail", "short_description", "genre",
        "platform", "publisher", "developer", "release_date", "game_url"
    ]
    cols = [c for c in cols if c in df.columns]
    df = df[cols].copy()

    # Convertir release_date a tipo fecha (DATE) para MySQL
    if "release_date" in df.columns:
        df["release_date"] = pd.to_datetime(df["release_date"], errors="coerce").dt.date
        df["release_date"] = df["release_date"].where(df["release_date"].notna(), None)

    # NULL -> "N/A" (o 0)
    df = df.fillna("N/A") 

    # 3) Load MySQL (idempotente por PK: id)
    db: Session = SessionLocal()
    try:
        inspector = inspect(db.get_bind())
        columnas_info = inspector.get_columns(Juego.__tablename__)
        columnas_actuales = {col["name"] for col in columnas_info}
        if "thumbnail" not in columnas_actuales:
            db.execute(text(f"ALTER TABLE {Juego.__tablename__} ADD COLUMN thumbnail VARCHAR(300)"))
            db.commit()
        columna_release = next((col for col in columnas_info if col["name"] == "release_date"), None)
        if columna_release is None:
            db.execute(text(f"ALTER TABLE {Juego.__tablename__} ADD COLUMN release_date DATE"))
            db.commit()
        elif not isinstance(columna_release["type"], (Date, mysql.DATE)):
            db.execute(text(f"ALTER TABLE {Juego.__tablename__} MODIFY COLUMN release_date DATE"))
            db.commit()

        procesados = 0

        for rec in df.to_dict(orient="records"):  # lista de dicts (1 por fila)
            game_id = int(rec["id"])

            existente = db.get(Juego, game_id)  # lookup por primary key [web:179]
            if existente is None:
                db.add(Juego(**rec)) # type: ignore
            else:
                for k, v in rec.items():
                    setattr(existente, k, v) # type: ignore

            procesados += 1

        db.commit()

        return {
            "mensaje": "Pipeline finalizado",
            "registros_procesados": int(procesados),
            "tabla_destino": Juego.__tablename__,
            "status": 200
        }
    except Exception:
        db.rollback()
        raise
    finally:
        db.close()


#---Reset
def reset_etl_storage() -> dict:
    """
    Endpoint C: limpia todo (Mongo raw + tabla MySQL).
    """
    # 1) Mongo: borrar todos los documentos
    mongo_result = mongo_collection.delete_many({})
    mongo_deleted = mongo_result.deleted_count  # [file:104]

    # 2) MySQL: contar filas y truncar tabla
    db: Session = SessionLocal()
    try:
        mysql_deleted = db.query(Juego).count()
        db.execute(text(f"TRUNCATE TABLE {Juego.__tablename__}"))
        db.commit()
    except Exception:
        db.rollback()
        raise
    finally:
        db.close()

    return {
        "mensaje": "Sistema reseteado correctamente",
        "mongo_docs_eliminados": int(mongo_deleted),
        "mysql_rows_eliminadas": int(mysql_deleted),
        "status": 200
    }
