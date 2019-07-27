from django.contrib.auth import get_user_model
from django.contrib.gis.db import models

User = get_user_model()


class Service(models.Model):
    provider = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=120)
    price = models.DecimalField(max_digits=8, decimal_places=2)
    polygon = models.PolygonField()

    class Meta:
        ordering = ["name"]
