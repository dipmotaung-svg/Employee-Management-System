from decimal import Decimal, InvalidOperation

from django import template

register = template.Library()


@register.filter
def rand(value):
    """Format a number as South African rand, e.g. 25000 -> R25,000.00"""
    try:
        amount = Decimal(value)
    except (InvalidOperation, TypeError, ValueError):
        return value
    return f"R{amount:,.2f}"