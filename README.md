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


## Requisitos
- Python 3.10+ (recomendado)
- MongoDB corriendo local o remoto
- MySQL corriendo local o remoto

Instala dependencias:
```bash
pip install -r requirements.txt
```

## Variables de entorno
Crea un archivo `.env` en la raíz (mismo nivel que `app/`) con tus credenciales.

Ejemplo (ajusta valores):
```env
# Mongo
MONGO_URI=mongodb://localhost:27017
MONGO_DB=laboratorio_etl
MONGO_COLLECTION=raw_data

# MySQL (ejemplo con pymysql)
DATABASE_URL=mysql+pymysql://USER:PASSWORD@localhost:3306/laboratorio_etl
```

> Nota: si tu `DATABASE_URL` usa `mysql+pymysql`, necesitas tener `pymysql` instalado (por ejemplo: `pip install pymysql`).

## Ejecutar el servidor
Desde la raíz del proyecto:
```bash
uvicorn app.main:app --reload
```

Si tuviste problemas de imports, puedes usar:
```bash
uvicorn --app-dir . app.main:app --reload
```

FastAPI expone documentación automática en:
- Swagger UI: `http://127.0.0.1:8000/docs`
- OpenAPI JSON: `http://127.0.0.1:8000/openapi.json`

## Endpoints (ETL)
Prefijo base:
```
/api/v1/etl
```

### 1) Extraer juegos
- **POST** `/api/v1/etl/extraer`
- Guarda datos crudos en MongoDB.
- Body (ejemplo):
```json
{ "cantidad": 50 }
```

Respuesta esperada (referencial):
```json
{
  "mensaje": "Datos extraídos y guardados en MongoDB",
  "cantidad": 50,
  "fuente": "FreeToGame API",
  "status": 201
}
```

### 2) Transformar y cargar
- **POST** `/api/v1/etl/transformar`
- No recibe body.
- Lee desde MongoDB, transforma y carga en MySQL (tabla `juegos`).
- Debe ser **idempotente** (repetirlo no debe duplicar filas).

Respuesta esperada (referencial):
```json
{
  "mensaje": "Transformación y carga completadas",
  "registros_procesados": 50,
  "tabla_destino": "juegos",
  "status": 200
}
```

### 3) Reset del ETL
- **DELETE** `/api/v1/etl/reset`
- Borra la colección en MongoDB y vacía la tabla en MySQL.

Respuesta esperada (referencial):
```json
{
  "mensaje": "Reset completado",
  "mongo_docs_eliminados": 50,
  "mysql_rows_eliminadas": 50,
  "status": 200
}
```

## Flujo recomendado de prueba
1) `DELETE /api/v1/etl/reset`
2) `POST /api/v1/etl/extraer` (ej. cantidad=50)
3) `POST /api/v1/etl/transformar`
4) Repite `POST /transformar` para validar idempotencia (no duplica).

## Postman
Puedes importar la colección de Postman (si aplica) y configurar la variable:
- `base_url = http://127.0.0.1:8000`

Requests típicos:
- `{{base_url}}/api/v1/etl/extraer`
- `{{base_url}}/api/v1/etl/transformar`
- `{{base_url}}/api/v1/etl/reset`

## Licencia
Ver archivo `LICENSE`.

## gracias por el curso profe :) ## 