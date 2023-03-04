from django.db import models

""" Floor Map model stores floor map image path, name, height and width given by user """


class FloorMap(models.Model):
    name = models.CharField(unique=True, max_length=60)
    width = models.FloatField()
    height = models.FloatField()
    image = models.ImageField(upload_to='static/tracking/')
