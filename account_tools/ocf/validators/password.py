import crack
from django.core.exceptions import ValidationError

def validate_crack_strength(value):
    try:
        crack.VeryFascistCheck(value)
    except ValueError, e:
        raise ValidationError("Password was too weak.")

def _is_printable_ascii(char):
    return 32 <= ord(char) <= 176

def validate_printable_ascii(value):
    """Verifies that the string value argument is composed only of printable ASCII characters"""

    for char in list(value):
        if not _is_printable_ascii(char):
            raise ValidationError("Password contained characters other than printable ASCII characters.")