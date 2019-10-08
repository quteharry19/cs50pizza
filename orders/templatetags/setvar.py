from django import template

register = template.Library()


@register.simple_tag
def get_num_top(name=None):
    if name.lower() == "cheese":
        num_top = 0
    elif name.lower() == "special":
        num_top = ""
    elif name[0].isnumeric():
        num_top = name[0]
    else:
        num_top = 0
    return num_top
