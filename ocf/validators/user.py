from ocf.utils import user_exists
from django.core.exceptions import ValidationError

def validate_unused_name(name):
    if not user_exists(name):
        raise ValidationError("OCF name is already used by someone else")