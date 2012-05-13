from ocf.utils import user_exists
from django.core.exceptions import ValidationError


def validate_name_characters(name):
    """Only lower-case letters are allowed in names"""
    error = "OCF name contains characters that aren't lower-case letters"
    for char in list(name):
        if not 97 <= ord(char) <= 122:
            # 97 is lower-case "a", 122 is lower-case "z"
            raise ValidationError(error)


def validate_unused_name(name):
    if user_exists(name):
        raise ValidationError("OCF name is already used by someone else")
