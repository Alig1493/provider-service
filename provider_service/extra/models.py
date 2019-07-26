from django.db import models


class Language(models.Model):
    name = models.CharField(max_length=10)

    def __str__(self):
        return self.name


class Currency(models.Model):
    name = models.CharField(max_length=10)

    def __str__(self):
        return self.name
