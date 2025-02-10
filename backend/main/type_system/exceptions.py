class TypeSystemException(Exception):
    """Base exception for type system errors"""
    pass

class TypeValidationError(TypeSystemException):
    """Raised when type validation fails"""
    pass

class TypeConversionError(TypeSystemException):
    """Raised when type conversion fails"""
    pass

class SchemaValidationError(TypeSystemException):
    """Raised when schema validation fails"""
    pass 