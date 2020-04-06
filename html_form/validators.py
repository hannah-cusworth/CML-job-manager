from django.core.exceptions import ValidationError

#does this need to return?
def validate_alpha(value):
    if not value.isalpha():
        raise ValidationError("Letters only please.")
    return value