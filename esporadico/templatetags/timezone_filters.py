from django import template
from datetime import datetime
import pytz

register = template.Library()

@register.filter
def local_datetime(value, format_string="d/m/Y H:i"):
    """
    Filtro para exibir datetime no fuso horário local (Brasília)
    """
    if not value:
        return ""
    
    # Se já é timezone-naive, formatar diretamente
    if not value.tzinfo:
        return value.strftime(format_string.replace('d', '%d').replace('m', '%m').replace('Y', '%Y').replace('H', '%H').replace('i', '%M'))
    
    # Se é timezone-aware, converter para Brasília
    sp_tz = pytz.timezone('America/Sao_Paulo')
    local_time = value.astimezone(sp_tz)
    return local_time.strftime(format_string.replace('d', '%d').replace('m', '%m').replace('Y', '%Y').replace('H', '%H').replace('i', '%M'))

@register.filter
def debug_datetime(value):
    """
    Filtro para debug - mostra informações completas do datetime
    """
    if not value:
        return "None"
    
    result = f"Valor: {value}, Tipo: {type(value)}"
    if hasattr(value, 'tzinfo'):
        result += f", TZ: {value.tzinfo}"
    
    return result
