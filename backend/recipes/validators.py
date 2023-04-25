import re

from django.core.exceptions import ValidationError


def validate_color(color):
    if not re.match(r'^#[0-9A-F]{6}$', color):
        raise ValidationError(
            'Допускается только HEX-код цвета в формате "#AABBCC"'
        )
