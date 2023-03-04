from django.db import models

from common.models import FloorMap
from employee.models import EmployeeRegistration


""" Zones model: """


class Zones(models.Model):
    zonename = models.CharField(max_length=20)
    x1 = models.FloatField()
    y1 = models.FloatField()
    x2 = models.FloatField()
    y2 = models.FloatField()
    floor = models.ForeignKey(FloorMap, on_delete=models.CASCADE)


""" ZoneTracking model: """


class ZoneTracking(models.Model):
    zoneid = models.ForeignKey(Zones, on_delete=models.CASCADE)
    tagid = models.ForeignKey(EmployeeRegistration, on_delete=models.CASCADE)
    timestamp = models.DateTimeField(null=True)


""" WeeklyZoneTracking model: """


class WeeklyZoneTracking(models.Model):
    zoneid = models.ForeignKey(Zones, on_delete=models.CASCADE)
    count = models.IntegerField()
    timestamp = models.DateTimeField(null=True)


""" MonthlyZoneTracking model: """


class MonthlyZoneTracking(models.Model):
    zoneid = models.ForeignKey(Zones, on_delete=models.CASCADE)
    count = models.IntegerField()
    timestamp = models.DateTimeField(null=True)
