from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .validators import validate_character_types, validate_minimum_length


class SignUpForm(UserCreationForm):
    password1 = forms.CharField(
        label="Пароль",
        widget=forms.PasswordInput,
        validators=[validate_minimum_length, validate_character_types],
        help_text="Минимум 2 буквы и 2 цифры",
    )

    class Meta:
        model = User
        fields = ["username", "email", "password1", "password2"]
        help_texts = {
            "username": "Обязательное поле.",
            "email": "Необязательно, но рекомендуется",
        }
        error_messages = {
            "username": {
                "unique": "Пользователь с таким именем уже существует.",
            },
        }

    error_messages = {
        "password_mismatch": "Пароли не совпадают. Пожалуйста, проверьте оба поля.",
    }


class LocationSearchForm(forms.Form):
    query = forms.CharField(
        label="",
        max_length=200,
        widget=forms.TextInput(
            attrs={
                "class": "search-input",
                "placeholder": "Введите название города или локации...",
                "autocomplete": "off",
            }
        ),
    )
