from django import template

register = template.Library()


@register.filter(name="addclass")
def addclass(field, css_class):
    """Adiciona uma classe CSS a um campo do formulário."""
    return field.as_widget(attrs={"class": css_class})
