from django.core.exceptions import ValidationError


def validate_username_not_me(value):
    """Запрещает использовать 'me' как имя пользователя."""
    if value.lower() == 'me':
        raise ValidationError('Использование имени "me" как логина запрещено.')
