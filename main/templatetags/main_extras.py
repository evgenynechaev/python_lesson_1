from django import template
from django.template.defaultfilters import stringfilter

register = template.Library()


@register.filter(is_safe=True)
@stringfilter
def label_with_classes(value, arg):
    print(value)
    return value.label_tag(attrs={'class': arg})
