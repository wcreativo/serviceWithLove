import os
from django import template


register = template.Library()


@register.simple_tag
def get_public_key(key):
    return os.environ.get(key)
