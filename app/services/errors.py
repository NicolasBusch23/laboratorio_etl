class PersonaNotFoundError(Exception):
    """Raised when a Persona entity is not found."""

class EmailAlreadyExistsError(Exception):
    """Raised when trying to use an email that already exists for another Persona."""