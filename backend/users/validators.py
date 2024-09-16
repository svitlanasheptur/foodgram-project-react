from django.core.exceptions import ValidationError

FORBIDDEN_USERNAME = 'me'


def validate_username_not_me(value):
    """Запрещает использовать 'me' как имя пользователя."""
    if value == FORBIDDEN_USERNAME:
        raise ValidationError(
            f'Использование имени "{FORBIDDEN_USERNAME}" как логина запрещено.'
        )
