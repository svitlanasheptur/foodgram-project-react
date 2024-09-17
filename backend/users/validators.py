from django.core.exceptions import ValidationError
from core.constraints import FORBIDDEN_USERNAME


def doc(docstring):
    """Декоратор для изменения строки документации функции."""
    def document(func):
        func.__doc__ = docstring
        return func
    return document


@doc(f"Запрещает использовать '{FORBIDDEN_USERNAME}' как имя пользователя.")
def validate_username_not_me(value):
    if value == FORBIDDEN_USERNAME:
        raise ValidationError(
            f'Использование имени "{FORBIDDEN_USERNAME}" как логина запрещено.'
        )
