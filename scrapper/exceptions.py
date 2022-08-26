
class CharacterNotFound(Exception):
    """Raised when a character can be found on the armory."""

    pass


class ApiDataError(Exception):
    """Raised when an API call return data in an unexpected format."""

    pass
