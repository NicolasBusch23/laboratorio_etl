from .database import engine, Base
from .controllers import etl_controller
from .error_handlers import register_exception_handlers
from fastapi import FastAPI

def create_app() -> FastAPI:
    """Application factory."""
    app = FastAPI(title="ETL FreeToGame API", version="1.0.0")

    # Register global exception handlers (domain → HTTP)
    register_exception_handlers(app)

    @app.on_event("startup") #Crea automáticamente las tablas definidas en models en caso de que no existan
    def on_startup() -> None:
        Base.metadata.create_all(bind=engine)

    @app.get("/health") #Permite probar que la app corra correctamente.
    def health() -> dict:
        return {"status": "ok"}

    app.include_router(etl_controller.router) #Conecta a la aplicación principal los endpoint definidos en el módulo etl_controller

    return app


app = create_app()
