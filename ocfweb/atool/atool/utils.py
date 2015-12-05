from django.core.exceptions import ValidationError


def wrap_validator(validator):
    """Wraps a validator which raises some kind of Exception, and instead
    returns a Django ValidationError with the same message.

    Useful for when you want to use validators from non-Django libraries.

    >>> validate_username('ocf')
    Exception: Username is reserved
    >>> validator = wrap_validator(validate_username)
    >>> validator('ocf')
    ValidationError: Username is reserved
    """
    def wrapped_validator(*args, **kwargs):
        try:
            validator(*args, **kwargs)
        except Exception as ex:
            raise ValidationError(ex)
    return wrapped_validator
