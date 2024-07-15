from django import template


register = template.Library()

@register.filter
def get_field_value(instance, field_name):
    return getattr(instance, field_name, '')

@register.filter
def fformsets(value):
    # Remove Spaces and make sure it is singular
    return value.replace(' ', '')[:-1]

@register.filter
def titlify(value):
    return value.replace('_', ' ').title()

@register.filter
def get_property(obj, prop):
    return getattr(obj, prop)

# Filters to check if field is a ForeignKey
# And to get url for the related model
@register.filter
def is_foreign_key(instance, field):
    try:
        return instance._meta.get_field(field).get_internal_type() == 'ForeignKey'
    except AttributeError:
        return False

@register.filter
def get_detail_url(instance, field):
    try:
        return instance._meta.get_field(field).related_model._meta.model_name + '-detail'
    except AttributeError:
        return ''

@register.filter
def get_foreign_key_value(instance, field):
    try:
        return getattr(instance, field).pk
    except AttributeError:
        return ''