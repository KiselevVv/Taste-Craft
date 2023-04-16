import re

from django.core.exceptions import ValidationError


def validate_username(username):
    if username == 'me':
        raise ValidationError(
            'Использовать имя me запрещено'
        )
    if not re.match(r'^[\w.@+-]+$', username):
        raise ValidationError(
            'Допустимо использовать только буквы, цифры и @/./+/-/_'
        )
