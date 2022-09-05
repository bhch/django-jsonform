from django.core.exceptions import ValidationError


class JSONSchemaValidationError(ValidationError):
    """Subclass of Django's ValidationError"""
    def __init__(self, message, code=None, params=None, error_map=None):
        super().__init__(message, code, params)
        self.error_map = error_map
