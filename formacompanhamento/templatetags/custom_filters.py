from django import template
import locale

register = template.Library()

# Definindo filtro de moeda
# No filtro customizado, altere para exibir sem casas decimais
@register.filter(name='currency')
def currency(value):
    try:
        # Defina a localidade para o Brasil
        locale.setlocale(locale.LC_ALL, 'pt_BR.UTF-8')
        # Formate o valor como moeda, mas sem casas decimais
        return locale.currency(value, grouping=True, symbol=True)[:-3]
    except (ValueError, TypeError):
        return value
    
    from django import template

from django import template

register = template.Library()

@register.filter
def get_field(form, field_name):
    return form[field_name]  


