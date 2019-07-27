import factory
from factory import SubFactory
from factory.fuzzy import FuzzyFloat

from provider_service.services.models import Service
from provider_service.users.tests.factories import UserFactory


class ServiceFactory(factory.DjangoModelFactory):
    provider = SubFactory(UserFactory)
    name = factory.Faker("word")
    price = FuzzyFloat(high=9999, low=1000)

    class Meta:
        model = Service
