import re

from django.core.exceptions import ValidationError


def validate_color(color):
    """
    Проверяет валидность HEX-кода цвета.
    :param color: HEX-код цвета для проверки.
    :return: ValidationError, если HEX-код цвета недопустим.
    """
    if not re.match(r'^#[0-9A-F]{6}$', color):
        raise ValidationError(
            'Допускается только HEX-код цвета в формате "#AABBCC"'
        )
