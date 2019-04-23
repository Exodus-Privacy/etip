from django import template

register = template.Library()


@register.simple_tag(takes_context=True)
def url_replace(context, field, value):
    """
    Utility function to replace the value of a specified parameter in URL
    """
    get_dict = context['request'].GET.copy()
    get_dict[field] = value
    return get_dict.urlencode()
