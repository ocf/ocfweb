import crack
from django.core.exceptions import ValidationError

def validate_password_strength(value):
    try:
        crack.VeryFascistCheck(value)
    except ValueError, e:
        raise ValidationError("Password was too weak.")
