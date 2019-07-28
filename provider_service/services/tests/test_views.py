from collections import OrderedDict

from django.urls import reverse

from rest_framework_gis.fields import GeoJsonDict

from provider_service.services.tests.factory import ServiceFactory
from provider_service.services.tests.test_utils import Utils
from provider_service.users.tests.factories import fake


# test data taken from:
# https://github.com/djangonauts/django-rest-framework-gis/
# blob/master/tests/django_restframework_gis_tests/test_fields.py


class TestServices(Utils):
    url = reverse("v1:services:list_create")
    name = fake.word()
    price = f"{12:.2f}"

    def test_create_service(self, auth_client, user):
        data = {
            "name": self.name,
            "price": self.price,
            "polygon": self.polygon_data
        }

        request = auth_client.post(self.url, data=data, format="json")

        assert request.status_code == 201

        expected_result = {
            "id": request.data.get("id"),
            "type": "Feature",
            "geometry":
                GeoJsonDict(
                    [("type", self.polygon_data["type"]), ("coordinates", self.polygon_data["coordinates"])]
                ),
            "properties": OrderedDict(
                [("provider", user.name), ("name", self.name), ("price", self.price)]
            )
        }

        assert request.data == expected_result

    def test_fetch_service_list(self, auth_client, user):
        ServiceFactory(provider=user, polygon=self.first_polygon)
        ServiceFactory(provider=user, polygon=self.second_polygon)

        request = auth_client.get(self.url)

        assert request.status_code == 200
        assert request.data.get("count") == 2

    def test_filter_service_list(self, auth_client, user):
        ServiceFactory(provider=user, polygon=self.first_polygon)
        ServiceFactory(provider=user, polygon=self.second_polygon)

        params = {
            "lat": -79.47887419545945,
            "long": 43.84581909379884
        }

        request = auth_client.get(self.url, data=params)

        assert request.status_code == 200
        assert request.data.get("count") == 1


class TestServiceDetails(Utils):

    def test_retrieve_single_service_data(self, auth_client, user):
        service = ServiceFactory(provider=user, polygon=self.first_polygon)
        ServiceFactory(provider=user, polygon=self.second_polygon)

        url = reverse("v1:services:details", args=[service.id])

        request = auth_client.get(url)

        assert request.status_code == 200
        assert request.data.get("id") == service.id

    def test_patch_service_data(self, auth_client, user):
        service = ServiceFactory(provider=user, polygon=self.first_polygon)

        url = reverse("v1:services:details", args=[service.id])

        request = auth_client.patch(url, data={"polygon": self.polygon_data}, format="json")

        assert request.status_code == 200

        expected_result = {
            "id": request.data.get("id"),
            "type": "Feature",
            "geometry":
                GeoJsonDict(
                    [("type", self.polygon_data["type"]), ("coordinates", self.polygon_data["coordinates"])]
                ),
            "properties": OrderedDict(
                [("provider", user.name), ("name", service.name), ("price", f"{service.price:.2f}")]
            )
        }

        assert request.data == expected_result

    def test_delete_service_data(self, auth_client, user):
        service = ServiceFactory(provider=user, polygon=self.first_polygon)

        url = reverse("v1:services:details", args=[service.id])

        request = auth_client.delete(url)

        assert request.status_code == 204
