from django.contrib.gis.geos import Point
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework_gis.pagination import GeoJsonPagination

from provider_service.services.models import Service
from provider_service.services.serializers import ServiceSerializer


class ServiceListCreateAPIView(ListCreateAPIView):
    """
    For GET request in batch operations,
    will take latitude nad longitude as query params to filter
    polygons according to the given point. Example,

    /api/v1/service/?lat=-79.47887419545945&long=43.84581909379884
    """
    pagination_class = GeoJsonPagination
    permission_classes = [IsAuthenticated]
    serializer_class = ServiceSerializer

    def get_queryset(self):
        queryset = Service.objects.filter(provider_id=self.request.user.id)
        lat = self.request.query_params.get("lat")
        lng = self.request.query_params.get("long")

        if (lat is not None) and (lng is not None):
            # In case the query params provide anything other than numbers
            try:
                return queryset.filter(polygon__contains=Point(float(lat), float(lng)))
            except ValueError:
                pass

        return queryset

    def perform_create(self, serializer):
        serializer.save(provider_id=self.request.user.id)


class ServiceRetrieveUpdateDestroyAPIView(RetrieveUpdateDestroyAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = ServiceSerializer

    def get_queryset(self):
        return Service.objects.filter(provider_id=self.request.user.id)
