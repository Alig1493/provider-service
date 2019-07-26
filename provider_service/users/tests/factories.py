import factory
from django.contrib.auth import get_user_model
from factory import SubFactory
from faker import Faker

from provider_service.extra.tests.factories import LanguageFactory, CurrencyFactory

fake = Faker()
User = get_user_model()


class UserFactory(factory.django.DjangoModelFactory):

    class Meta:
        model = User

    email = factory.Faker("email")
    phone_number = factory.Faker("phone_number")
    language = SubFactory(LanguageFactory)
    currency = SubFactory(CurrencyFactory)
    password = factory.PostGenerationMethodCall("set_password", "test_pass")
