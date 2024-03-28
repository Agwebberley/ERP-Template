from django import template

register = template.Library()

@register.filter(name='get_field_value')
def get_field_value(item, field_name):
    return getattr(item, field_name)

@register.filter(name='replace')
def replace(value, arg):
    # arg should be in the format of 'old,new'
    old, new = arg.split(',')
    newv = value.replace(old, new)

    # Remove the word get
    if newv.startswith('get'):
        newv = newv[3:]
    
    return newv