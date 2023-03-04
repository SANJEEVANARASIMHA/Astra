from django.db import models

from common.models import FloorMap
from gateway.models import MasterGateway

""" TemperatureHumidity model:
    stores sensor id, coordinates and floor id where it is placed """


class TemperatureHumidity(models.Model):
    macid = models.CharField(unique=True, max_length=20)
    temperature = models.FloatField()
    humidity = models.FloatField()
    lastseen = models.DateTimeField(auto_now=True)
    battery = models.FloatField()
    floor = models.ForeignKey(FloorMap, on_delete=models.CASCADE)
    x1 = models.FloatField(default=None, null=True)
    y1 = models.FloatField(default=None, null=True)
    x2 = models.FloatField(default=None, null=True)
    y2 = models.FloatField(default=None, null=True)


""" DailyTemperatureHumidty model"""


class DailyTemperatureHumidity(models.Model):
    temperature = models.FloatField()
    humidity = models.FloatField()
    timestamp = models.DateTimeField(auto_now=True)
    asset = models.ForeignKey(TemperatureHumidity, on_delete=models.CASCADE)


""" weeklyTemperatureHumidty model"""


class WeeklyTemperatureHumidity(models.Model):
    temperature = models.FloatField()
    humidity = models.FloatField()
    timestamp = models.DateTimeField(auto_now=True)
    asset = models.ForeignKey(TemperatureHumidity, on_delete=models.CASCADE)


""" MonthlyTemperatureHumidty model"""


class MonthlyTemperatureHumidity(models.Model):
    temperature = models.FloatField()
    humidity = models.FloatField()
    timestamp = models.DateTimeField(auto_now=True)
    asset = models.ForeignKey(TemperatureHumidity, on_delete=models.CASCADE)


""" IRQ model:
    stores sensor id, lastseen """


class IAQ(models.Model):
    macid = models.CharField(unique=True, max_length=20)
    lastseen = models.DateTimeField(auto_now=True)
    battery = models.FloatField()
    co2 = models.FloatField()
    tvoc = models.FloatField()
    floor = models.ForeignKey(FloorMap, on_delete=models.CASCADE)
    x = models.FloatField()
    y = models.FloatField()


""" DailyIAQ model"""


class DailyIAQ(models.Model):
    co2 = models.FloatField()
    tvoc = models.FloatField()
    battery = models.FloatField()
    timestamp = models.DateTimeField(auto_now=True)
    asset = models.ForeignKey(IAQ, on_delete=models.CASCADE)


""" WeeklyIAQ model"""


class WeeklyIAQ(models.Model):
    co2 = models.FloatField()
    tvoc = models.FloatField()
    timestamp = models.DateTimeField(auto_now=True)
    asset = models.ForeignKey(IAQ, on_delete=models.CASCADE)


""" MonthlyIAQ model"""


class MonthlyIAQ(models.Model):
    co2 = models.FloatField()
    tvoc = models.FloatField()
    timestamp = models.DateTimeField(auto_now=True)
    asset = models.ForeignKey(IAQ, on_delete=models.CASCADE)


class MultiSensor(models.Model):
    MACID = models.CharField(max_length=20)
    Temp = models.FloatField()
    Humi = models.FloatField()
    Co2 = models.FloatField()
    PM1 = models.FloatField()
    PM2 = models.FloatField()
    PM4 = models.FloatField()
    PM10 = models.FloatField()
    NC0 = models.FloatField()
    NC1 = models.FloatField()
    NC2 = models.FloatField()
    NC4 = models.FloatField()
    NC10 = models.FloatField()
    PtSize = models.FloatField()
    O2 = models.FloatField()
    VOC = models.FloatField()
    timestamp = models.DateTimeField(auto_now=True)


class MultiSensorDetails(models.Model):
    master = models.ForeignKey(MasterGateway, on_delete=models.CASCADE)
    MACID = models.CharField(max_length=20)
    Temp = models.FloatField()
    Humi = models.FloatField()
    Co2 = models.FloatField()
    PM1 = models.FloatField()
    PM2 = models.FloatField()
    PM4 = models.FloatField()
    PM10 = models.FloatField()
    NC0 = models.FloatField()
    NC1 = models.FloatField()
    NC2 = models.FloatField()
    NC4 = models.FloatField()
    NC10 = models.FloatField()
    PtSize = models.FloatField()
    O2 = models.FloatField()
    VOC = models.FloatField()
    timestamp = models.DateTimeField(auto_now=True)
