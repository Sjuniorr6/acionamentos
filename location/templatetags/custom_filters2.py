from django import template

register = template.Library()

@register.filter(name='float_dot')
def float_dot(value, decimals=6):
    """
    Converte 'value' em float e formata com ponto decimal,
    sempre com 'decimals' casas decimais.
    Exemplo: 1234.56789 -> "1234.567890"
    """
    if value is None:
        return ''
    try:
        value_float = float(value)
    except (ValueError, TypeError):
        return str(value)
    # Força o formato com ponto e X decimais
    return f"{value_float:.{decimals}f}"
