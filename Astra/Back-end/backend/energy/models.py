from django.db import models
# Create your models here.


class EnergyTracking(models.Model):
    tag = models.CharField(max_length=100)
    voltage = models.FloatField()
    energy = models.FloatField()
    current = models.FloatField()
    powerFactor = models.FloatField(default=0)
    timestamp = models.DateTimeField()


class VehicleTracking(models.Model):
    tag = models.CharField(max_length=100)
    vehicle_status = models.BooleanField()
    timestamp = models.DateTimeField()


class PassiveAsset(models.Model):
    tag = models.CharField(max_length=100)
    status = models.BooleanField()
    timestamp = models.DateTimeField()
