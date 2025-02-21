from django.urls import path
from .views import traccar_webhook, location_list, device_location, register_device,latest_location

urlpatterns = [
    path('webhook/', traccar_webhook, name='traccar_webhook'),
    path('list/', location_list, name='location_list'),
    path('device/<str:device_id>/', device_location, name='device_location'),
    path('register/', register_device, name='register_device'),
    path('latest/', latest_location, name='latest_location'),
]
