from rest_framework.relations import SlugRelatedField
from rest_framework_gis.serializers import GeoFeatureModelSerializer

from provider_service.services.models import Service


class ServiceSerializer(GeoFeatureModelSerializer):
    provider = SlugRelatedField(read_only=True, slug_field="name")

    class Meta:
        model = Service
        geo_field = "polygon"
        fields = "__all__"
