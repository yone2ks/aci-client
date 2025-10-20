"""
ACI Client custom exceptions
"""


class ACIClientError(Exception):
    """Base exception for ACI Client"""

    pass


class ConnectionError(ACIClientError):
    """Raised when connection to APIC fails"""

    pass


class AuthenticationError(ACIClientError):
    """Raised when authentication fails"""

    pass


class QueryError(ACIClientError):
    """Raised when query execution fails"""

    pass


class ConfigError(ACIClientError):
    """Raised when configuration commit fails"""

    pass


class ValidationError(ACIClientError):
    """Raised when input validation fails"""

    pass


class ResourceNotFoundError(ACIClientError):
    """Raised when requested resource is not found"""

    pass
