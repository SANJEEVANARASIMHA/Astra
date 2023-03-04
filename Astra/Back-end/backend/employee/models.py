from django.db import models
from common.models import FloorMap

""" EmployeeTag model: """

#
# class EmployeeTag(models.Model):
#     tagid = models.CharField(unique=True, max_length=20)
#     battery = models.FloatField()
#     lastseen = models.DateTimeField(auto_now=True)
#     x = models.FloatField()
#     y = models.FloatField()
#     floor = models.ForeignKey(FloorMap, on_delete=models.SET_NULL, null=True)


""" EmployeeRegistration model: """


#
# class EmployeeRegistration(models.Model):
#     tagid = models.ForeignKey(EmployeeTag, on_delete=models.CASCADE, null=True)
#     name = models.CharField(max_length=100)
#     empid = models.CharField(max_length=100)
#     email = models.CharField(max_length=254)
#     phoneno = models.CharField(max_length=12)
#     address = models.CharField(max_length=200)
#     intime = models.DateTimeField()


class EmployeeRegistration(models.Model):
    name = models.CharField(max_length=100)
    empid = models.CharField(max_length=100, unique=True, null=False, default=None)
    email = models.CharField(max_length=254, unique=True, null=False, default=None)
    phoneno = models.CharField(max_length=12, unique=True, null=False, default=None)
    role = models.CharField(max_length=200, default=None)
    tagid = models.CharField(unique=True, max_length=20, default=None)
    battery = models.FloatField(null=True, default=None)
    x = models.FloatField(default=0.0, null=True)
    y = models.FloatField(default=0.0, null=True)
    floor = models.ForeignKey(FloorMap, on_delete=models.SET_NULL, null=True)
    date = models.DateTimeField(auto_now_add=True, null=True)
    intime = models.DateTimeField(auto_now_add=True)
    # assigneddate = models.DateTimeField(auto_now_add=True, default=None)
    lastseen = models.DateTimeField(auto_now_add=True)


class EmployeeHistory(models.Model):
    emp = models.ForeignKey(EmployeeRegistration, on_delete=models.SET_NULL, null=True)
    floor = models.ForeignKey(FloorMap, on_delete=models.SET_NULL, null=True)
    x = models.FloatField(default=0.0, null=True)
    y = models.FloatField(default=0.0, null=True)
    battery = models.FloatField(null=True, default=None)
    lastseen = models.DateTimeField(auto_now_add=True)


""" DistanceTracking model: """


class DistanceTracking(models.Model):
    tag1 = models.ForeignKey(EmployeeRegistration, on_delete=models.CASCADE, related_name="tag1")
    tag2 = models.ForeignKey(EmployeeRegistration, on_delete=models.CASCADE, related_name="tag2")
    distance = models.IntegerField()
    timestamp = models.DateTimeField()


""" DistanceCalculation model """


class DistanceCalculation(models.Model):
    empid = models.CharField(max_length=100)
    name1 = models.CharField(max_length=100)
    name2 = models.CharField(max_length=100)
    starttime = models.DateTimeField()
    endtime = models.DateTimeField()
    duration = models.CharField(max_length=50)

#
# class File(models.Model):
#     name = models.CharField(max_length=100)
#     role= models.CharField(max_length=200, default=None)
#     tagid = models.CharField(unique=True, max_length=20, default=None)
#     battery = models.FloatField(null=True, default=None)
#     x = models.FloatField(default=None, null=True)
#     y = models.FloatField(default=None, null=True)
#     floor = models.ForeignKey(FloorMap, on_delete=models.SET_NULL, null=True)
#     intime = models.DateTimeField(auto_now_add=True)
#     lastseen = models.DateTimeField(auto_now=True)
#
#     def __str__(self):
#         return self.name
