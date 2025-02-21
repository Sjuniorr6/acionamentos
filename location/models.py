from django.db import models

# Create your models here.
# location/models.py

from django.db import models

class Device(models.Model):
    device_id = models.CharField(max_length=100, unique=True)
    registered_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.device_id

class Location(models.Model):
    device_id = models.CharField(max_length=100)
    latitude = models.FloatField()
    longitude = models.FloatField()
    timestamp = models.DateTimeField()

    speed = models.FloatField(null=True, blank=True)
    bearing = models.FloatField(null=True, blank=True)
    altitude = models.FloatField(null=True, blank=True)
    accuracy = models.FloatField(null=True, blank=True)
    battery = models.IntegerField(null=True, blank=True)
    is_charging = models.BooleanField(default=False)

    def __str__(self):
        return f"Location {self.id} - {self.device_id}"
