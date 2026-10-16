from decimal import Decimal, InvalidOperation

from django import template

register = template.Library()


@register.filter
def rand(value):
    try:
        amount = Decimal(value)
    except (InvalidOperation, TypeError, ValueError):
        return value
    return f"R{amount:,.2f}"