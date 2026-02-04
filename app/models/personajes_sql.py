from sqlalchemy import Column, String, Text, Boolean, Integer, Date, DateTime, func
from ..database import Base


class Juego(Base):
    """Modelo SQLAlchemy para la tabla de juegos."""
    __tablename__ = "juegos"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(200))
    thumbnail = Column(String(300))
    short_description = Column(String(500))
    genre = Column(String(100))
    platform = Column(String(100))
    publisher = Column(String(100))
    developer = Column(String(100))
    release_date = Column(Date)
    game_url = Column(String(300))
    
