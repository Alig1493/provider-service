from django.contrib.gis.db import models


class Service(models.Model):
    name = models.CharField(max_length=120)
    price = models.DecimalField(max_digits=8, decimal_places=2)
    polygon = models.PolygonField()
