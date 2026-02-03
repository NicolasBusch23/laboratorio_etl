from pydantic import BaseModel, Field

class ExtractRequest(BaseModel):
    """
    Schema de entrada para el endpoint EXTRACT.
    """
    cantidad: int = Field(
    ..., # Campo obligatorio: el usuario debe enviarlo sí o sí
    gt = 0,  # gt = greater than → El valor debe ser mayor que 0
    description = "Cantidad de registros a extraer"  # Texto visible en /docs
)
    
class TransformResponse(BaseModel):
    """
    Schema de salida para el endpoint TRANSFORM.
    """
    mensaje: str
    registros_procesados: int
    tabla_destino: str
    status: int