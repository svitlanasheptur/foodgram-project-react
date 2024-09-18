from django.core.exceptions import ValidationError

from core.constraints import FORBIDDEN_USERNAME
from core.decorators import doc


@doc(f"Запрещает использовать '{FORBIDDEN_USERNAME}' как имя пользователя.")
def validate_username_not_me(value):
    """Запрещает использовать определённое имя пользователя."""
    if value == FORBIDDEN_USERNAME:
        raise ValidationError(
            f'Использование имени "{FORBIDDEN_USERNAME}" как логина запрещено.'
        )
