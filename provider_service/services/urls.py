from django.conf.urls import url

from provider_service.services.views import ServiceListCreateAPIView, ServiceRetrieveUpdateDestroyAPIView

app_name = "services"


urlpatterns = [
    url(r"^$", ServiceListCreateAPIView.as_view(), name="list_create"),
    url(r"^(?P<pk>[0-9]+)/$", ServiceRetrieveUpdateDestroyAPIView.as_view(), name="details"),
]
