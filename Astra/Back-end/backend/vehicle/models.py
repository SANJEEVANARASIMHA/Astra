from django.db import models


class VehicleTracking(models.Model):
    mac = models.CharField(max_length=50)
    x = models.FloatField()
    y = models.FloatField()
    battery = models.FloatField()
    temperature = models.FloatField()
    humidity = models.FloatField()
    vehicleid = models.CharField(max_length=50)
    gateway = models.CharField(max_length=50)
    lastseen = models.DateTimeField()
    timestamp = models.IntegerField()


class TemperatureTracking(models.Model):
    temperature = models.FloatField()
    gateway = models.CharField(max_length=50)
    lastseen = models.DateTimeField()
