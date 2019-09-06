from django import template

register = template.Library()


@register.simple_tag
def get_num_top(val=None):
    return val

def letInt(val=None):
    try:
        return int(val)
    except ValueError:
        return False
    