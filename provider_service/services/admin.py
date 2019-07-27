# Register your models here.
from django.contrib.gis import admin
from django.contrib.gis.admin import OSMGeoAdmin

from provider_service.services.models import Service


class ServiceAdmin(OSMGeoAdmin):
    list_display = ("name", "price", "polygon")


admin.site.register(Service, ServiceAdmin)
