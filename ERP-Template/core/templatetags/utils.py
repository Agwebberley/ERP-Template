from django import template


register = template.Library()

@register.filter
def get_field_value(instance, field_name):
    return getattr(instance, field_name, '')

@register.filter
def fformsets(value):
    # Remove Spaces and make sure it is singular
    return value.replace(' ', '')[:-1]