# Laboratorio ETL - FastAPI (Juegos)

Backend en **FastAPI** que implementa un flujo ETL para juegos:
1) **Extracción**: consume una API pública de juegos y guarda los datos crudos en **MongoDB**.
2) **Transformación + Carga**: lee desde MongoDB, transforma (aplana/limpia) y carga en **MySQL** en una tabla plana.
3) **Reset**: limpia el almacenamiento (MongoDB + MySQL) para repetir pruebas.

## Tecnologías
- Python + FastAPI (API REST)
- MongoDB (staging / datos crudos)
- MySQL (tabla destino)
- SQLAlchemy (ORM)
- Uvicorn (servidor ASGI)

## Estructura (referencial)
Proyecto organizado en múltiples archivos bajo `app/` (patrón recomendado para FastAPI):

- `app/main.py` (instancia `app = FastAPI()`)
- `app/controllers/etl_controller.py` (rutas)
- `app/services/etl_service.py` (lógica ETL)
- `app/models/personajes_sql.py` (modelo SQLAlchemy; tabla `juegos`)
- `app/views/schemas.py` (schemas Pydantic)
- `app/database.py` (engine/SessionLocal/Base)
- `.env` (variables de entorno)

