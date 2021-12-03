class HousingUnitBaseError(Exception):
    message: str = None
    error_type: str = None
    status_code: int = 400


class ArgumentError(HousingUnitBaseError):
    message = "Argument error."
    error_type = "ArgumentError"


class InvalidArgumentError(ArgumentError):
    message = "Invalid argument error."
    error_type = "InvalidArgumentError"


class NoneArgumentError(ArgumentError):
    message = "Missing argument error."
    error_type = "MissingArgumentError"


class ValidationError(HousingUnitBaseError):
    message = "Validation error."
    error_type = "ValidationError"
