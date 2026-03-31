import re
from django.core.exceptions import ValidationError


def validate_minimum_length(value, min_length=4):
    if len(value) < min_length:
        raise ValidationError(
            f"Этот пароль слишком короткий. Он должен содержать минимум {min_length} символов."
        )


def validate_character_types(value):
    letters = len(re.findall(r"[A-Za-z]", value))
    digits = len(re.findall(r"\d", value))

    if letters < 2 or digits < 2:
        raise ValidationError(
            "Пароль должен содержать минимум 2 буквы (латинские) и 2 цифры."
        )
