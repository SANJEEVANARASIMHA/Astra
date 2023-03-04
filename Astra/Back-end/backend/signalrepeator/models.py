from django.db import models

""" SignalRepeator model:
    stores sensor id, lastseen """
class SignalRepeator(models.Model):
    macid = models.CharField(unique=True, max_length=20)
    lastseen = models.DateTimeField(auto_now=True)
