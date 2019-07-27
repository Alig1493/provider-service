from collections import OrderedDict

from django.contrib.gis.geos import Polygon
from django.urls import reverse

from rest_framework_gis.fields import GeoJsonDict

from provider_service.services.tests.factory import ServiceFactory
from provider_service.users.tests.factories import fake

# test data taken from:
# https://github.com/djangonauts/django-rest-framework-gis/
# blob/master/tests/django_restframework_gis_tests/test_fields.py

POLYGON_DATA = {
    "type": "Polygon",
    "coordinates": [
        [
            [-84.3228, 34.9895],
            [-82.6062, 36.0335],
            [-82.6062, 35.9913],
            [-82.6062, 35.9791],
            [-82.5787, 35.9613],
            [-82.5677, 35.9513],
            [-84.2211, 34.9850],
            [-84.3228, 34.9895]
        ],
        [
            [-75.6903, 35.7420],
            [-75.5914, 35.7420],
            [-75.7067, 35.7420],
            [-75.6903, 35.7420]
        ],
    ]
}


class TestServices:

    url = reverse("v1:services:list_create")
    name = fake.word()
    price = f"{12:.2f}"

    first_polygon = Polygon(((0, 0), (0, 10), (10, 10), (0, 10), (0, 0)),
                            ((4, 4), (4, 6), (6, 6), (6, 4), (4, 4)))
    second_polygon = Polygon(((10, 10), (10, 20), (20, 20), (10, 20), (10, 10)),
                            ((14, 14), (14, 16), (16, 16), (16, 14), (14, 14)))

    def test_create_service(self, auth_client, user):
        data = {
            "name": self.name,
            "price": self.price,
            "polygon": POLYGON_DATA
        }

        request = auth_client.post(self.url, data=data, format="json")

        assert request.status_code == 201

        expected_result = {
            "id": request.data.get("id"),
            "type": "Feature",
            "geometry":
                GeoJsonDict(
                    [("type", POLYGON_DATA["type"]), ("coordinates", POLYGON_DATA["coordinates"])]
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
            "lat": 15,
            "long": 15
        }

        request = auth_client.get(self.url, params=params)

        print(request.data)
