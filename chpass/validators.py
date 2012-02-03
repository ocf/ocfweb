import crack
from django.core.exceptions import ValidationError

def validate_password_length(value):
    if len(value) < 8:
        raise ValidationError("Password must be longer than 8 characters.")

def validate_password_strength(value):
    try:
        crack.VeryFascistCheck(value)
    except ValueError, e:
        raise ValidationError("Password was too weak.")
