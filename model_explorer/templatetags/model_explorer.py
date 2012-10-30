from django import template

register = template.Library()

@register.inclusion_tag('model_explorer/chart_form.html')
def chart_form(cl):
    """
    Displays a search form for searching the list.
    """
    return {
        'cl': cl,
    }
