from typing import Any
from typing import Callable

from django import forms
from django.core.exceptions import ValidationError


class Form(forms.Form):
    """An OCF-flavored Django form that works well with Bootstrap."""

    error_css_class = 'error'
    required_css_class = 'required'


def wrap_validator(validator: Callable[..., Any]) -> Callable[..., None]:
    """Wraps a validator which raises some kind of Exception, and instead
    returns a Django ValidationError with the same message.

    Useful for when you want to use validators from non-Django libraries.

    >>> validate_username('ocf')
    Exception: Username is reserved
    >>> validator = wrap_validator(validate_username)
    >>> validator('ocf')
    ValidationError: Username is reserved
    """
    def wrapped_validator(*args: Any, **kwargs: Any) -> None:
        try:
            validator(*args, **kwargs)
        except Exception as ex:
            raise ValidationError(ex)
    return wrapped_validator
