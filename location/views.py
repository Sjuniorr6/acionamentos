import traceback
from datetime import datetime

from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse

from .models import Device, Location
import traceback
from datetime import datetime

from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from django.shortcuts import render

from .models import Device, Location


@csrf_exempt
def traccar_webhook(request):
    """
    Recebe dados do Traccar Client via query string.
    Exemplo de URL:
    /api/traccar/webhook/?id=sidnei&timestamp=1740078445&lat=-23.636356&lon=-46.512661
                         &speed=0&bearing=0&altitude=800.0866&accuracy=7.63&batt=85&charge=true
    """
    if request.method == 'POST':
        try:
            # Coletando os parâmetros enviados via query string
            device_id = request.GET.get('id')  # "id" no Traccar
            timestamp_str = request.GET.get('timestamp')
            lat_str = request.GET.get('lat')
            lon_str = request.GET.get('lon')
            speed_str = request.GET.get('speed')
            bearing_str = request.GET.get('bearing')
            altitude_str = request.GET.get('altitude')
            accuracy_str = request.GET.get('accuracy')
            batt_str = request.GET.get('batt')
            charge_str = request.GET.get('charge')

            # Validação básica
            if not device_id:
                return JsonResponse({'status': 'error', 'message': 'Parâmetro "id" ausente'}, status=400)

            # Substitui vírgulas por pontos ANTES de converter para float
            if lat_str:
                lat_str = lat_str.replace(',', '.')
            if lon_str:
                lon_str = lon_str.replace(',', '.')

            # Conversão dos parâmetros (strings) para tipos adequados
            latitude = float(lat_str) if lat_str else 0.0
            longitude = float(lon_str) if lon_str else 0.0
            speed = float(speed_str) if speed_str else 0.0
            bearing = float(bearing_str) if bearing_str else 0.0
            altitude = float(altitude_str) if altitude_str else 0.0
            accuracy = float(accuracy_str) if accuracy_str else 0.0
            battery = int(batt_str) if batt_str else 0
            is_charging = (charge_str.lower() == "true") if charge_str else False

            # Converter timestamp para datetime, se for um UNIX epoch (em segundos)
            if timestamp_str:
                timestamp = datetime.fromtimestamp(int(timestamp_str))
            else:
                # Se não vier timestamp, usamos o horário atual
                timestamp = datetime.now()

            # Registrar (ou obter) o dispositivo
            device, created = Device.objects.get_or_create(device_id=device_id)

            # Criar registro de localização
            location = Location.objects.create(
                device_id=device.device_id,
                latitude=latitude,
                longitude=longitude,
                timestamp=timestamp,
                speed=speed,
                bearing=bearing,
                altitude=altitude,
                accuracy=accuracy,
                battery=battery,
                is_charging=is_charging,
            )

            return JsonResponse({'status': 'success', 'id': location.id}, status=200)

        except Exception as e:
            traceback.print_exc()
            return JsonResponse({'status': 'error', 'message': str(e)}, status=400)

    # Se não for POST, retorna 405
    return JsonResponse({'status': 'error', 'message': 'Método não permitido'}, status=405)


def location_list(request):
    """
    Lista todas as localizações em ordem do mais recente para o mais antigo
    e renderiza o template 'location_list.html'.
    """
    locations = Location.objects.all().order_by('-timestamp')
    return render(request, 'location_list.html', {'locations': locations})




from django.shortcuts import render
from .models import Location

def location_list(request):
    locations = Location.objects.all().order_by('-timestamp')
    return render(request, 'location_list.html', {'locations': locations})



from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
import json
from .models import Device

@csrf_exempt
def register_device(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            device_id = data.get('deviceId')
            name = data.get('name', '')  # opcional
            if not device_id:
                return JsonResponse({'status': 'error', 'message': 'deviceId é obrigatório'}, status=400)
            
            device, created = Device.objects.get_or_create(device_id=device_id, defaults={'name': name})
            if created:
                message = 'Dispositivo registrado com sucesso'
            else:
                message = 'Dispositivo já estava registrado'
            
            return JsonResponse({'status': 'success', 'message': message, 'device': device.device_id}, status=200)
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)}, status=400)
    return JsonResponse({'status': 'error', 'message': 'Método não permitido'}, status=405)



# location/templatetags/custom_filters.py

from django import template

register = template.Library()

@register.filter(name='replace_comma')
def replace_comma(value):
    """
    Substitui todas as vírgulas (,) por pontos (.) em uma string.
    Exemplo: "-23,636356" -> "-23.636356"
    """
    if value:
        return value.replace(',', '.')
    return value




from django.http import JsonResponse
from .models import Location

def device_location(request, device_id):
    # Filtra as localizações do dispositivo e pega o registro mais recente
    location = Location.objects.filter(device_id=device_id).order_by('-timestamp').first()
    if location:
        data = {
            'device_id': location.device_id,
            'latitude': location.latitude,
            'longitude': location.longitude,
            'timestamp': location.timestamp,
        }
        return JsonResponse(data, status=200)
    else:
        return JsonResponse({'error': 'Localização não encontrada para o dispositivo informado'}, status=404)



# location/views.py
from django.shortcuts import render
from .models import Location

def agente_location(request, device_id):
    # Exemplo: pegar o último registro do dispositivo
    location = Location.objects.filter(device_id=device_id).order_by('-timestamp').first()
    
    # Se não houver registro, podemos tratar ou passar None
    return render(request, 'agente_map.html', {'location': location})




# location/views.py

from django.shortcuts import render
from .models import Location

def latest_location(request):
    # Ordena as localizações do mais recente para o mais antigo e pega a primeira
    location = Location.objects.order_by('-timestamp').first()

    # Se não houver nenhuma localização, 'location' será None
    return render(request, 'latest_location.html', {'location': location})





def location_list(request):
    devices = Location.objects.values_list('device_id', flat=True).distinct()
    locations = []
    for d in devices:
        # pega os 2 mais recentes deste device
        locs = Location.objects.filter(device_id=d).order_by('-timestamp')[:2]
        locations.extend(locs)
    
    # Agora 'locations' é uma lista Python, podemos ordenar de novo
    locations.sort(key=lambda x: x.timestamp, reverse=True)
    return render(request, 'location_list.html', {'locations': locations})




# location/templatetags/custom_filters.py
from django import template

register = template.Library()

@register.filter(name='float_limit10')
def float_limit10(value):
    """
    Converte 'value' em float e retorna uma string com no máximo 10 caracteres,
    incluindo sinal e ponto decimal.
    Exemplo: -23.63649 => '-23.63649'
    """
    if value is None:
        return ''
    try:
        f = float(value)
    except (ValueError, TypeError):
        return str(value)
    
    # Formata com 8 casas decimais (ou quantas quiser)
    s = f"{f:.8f}"
    # Corta a string em no máximo 10 chars
    return s[:10]
