from django.db import models


class Sensors(models.Model):
    tagid = models.CharField(default=None, max_length=100)
    baseValue = models.FloatField(default=0.0, null=True)
    currentValue = models.FloatField(default=0.0, null=True)
    previousValue = models.FloatField(default=0.0, null=True)
    currentDiff = models.FloatField(default=0.0, null=True)
    previousDiff = models.FloatField(default=0.0, null=True)
    reading = models.FloatField(default=0.0, null=True)
    distancelader = models.FloatField(default=0.0, null=True)
    dcstatus = models.IntegerField(default=0, null=True)
    battery = models.FloatField(default=0.0, null=True)
    timestamp = models.DateTimeField(auto_now=True)
    display = models.FloatField(default=0, null=True)


class SensorReading(models.Model):
    tagid = models.ForeignKey(Sensors, on_delete=models.CASCADE, null=True)
    reading = models.FloatField(default=0.0, null=True)
    distancelader = models.FloatField(default=0.0, null=True)
    dcstatus = models.IntegerField(default=0, null=True)
    battery = models.FloatField(default=0.0, null=True)
    timestamp = models.DateTimeField(auto_now=True)
