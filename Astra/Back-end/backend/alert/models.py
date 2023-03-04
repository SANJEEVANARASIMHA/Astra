from django.db import models

# Create your models here.
from common.models import FloorMap
from employee.models import EmployeeRegistration


class Alert(models.Model):
    value = models.IntegerField()
    timestamp = models.DateTimeField()
    asset = models.ForeignKey(EmployeeRegistration, on_delete=models.CASCADE)
    floor = models.ForeignKey(FloorMap, on_delete=models.CASCADE, default=None)
    lastseen = models.DateTimeField(default=None)
