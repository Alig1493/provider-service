from django.contrib.gis.geos import Point
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework_gis.pagination import GeoJsonPagination

from provider_service.services.models import Service
from provider_service.services.serializers import ServiceSerializer


class ServiceListCreateAPIView(ListCreateAPIView):
    pagination_class = GeoJsonPagination
    permission_classes = [IsAuthenticated]
    serializer_class = ServiceSerializer

    def get_queryset(self):
        queryset = Service.objects.filter(provider_id=self.request.user.id)
        lat = self.request.query_params.get("lat")
        lng = self.request.query_params.get("long")

        if lat and lng:
            queryset = queryset.filter(polygon__contains=Point(float(lat), float(lng)))

        return queryset

    def perform_create(self, serializer):
        serializer.save(provider_id=self.request.user.id)


class ServiceRetrieveUpdateDestroyAPIView(RetrieveUpdateDestroyAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = ServiceSerializer

    def get_queryset(self):
        return Service.objects.filter(provider_id=self.request.user.id)
