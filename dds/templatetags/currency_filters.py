from decimal import Decimal, InvalidOperation
from django import template

register = template.Library()

@register.filter
def rubles(value):
    try:
        amount = Decimal(value)
    except (TypeError, ValueError, InvalidOperation):
        return value

    formatted = f"{amount:.2f}"
    integer_part, fraction = formatted.split('.')
    integer_part = integer_part.replace('-', '')
    groups = []
    while integer_part:
        groups.append(integer_part[-3:])
        integer_part = integer_part[:-3]
    integer_with_spaces = ' '.join(reversed(groups))
    if formatted.startswith('-'):
        integer_with_spaces = f'-{integer_with_spaces}'

    if fraction == '00':
        return f"{integer_with_spaces} р."
    return f"{integer_with_spaces},{fraction} р."
