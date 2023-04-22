import re

from django.core.exceptions import ValidationError


def validate_username(username):
    usernames = ['me', 'subscriptions', 'activation', 'resend_activation',
                 'reset_password', 'reset_username', 'set_password',
                 'set_username']
    if username in usernames:
        raise ValidationError(
            'Использовать имя запрещено'
        )
    if not re.match(r'^[\w.@+-]+$', username):
        raise ValidationError(
            'Допустимо использовать только буквы, цифры и @/./+/-/_'
        )
