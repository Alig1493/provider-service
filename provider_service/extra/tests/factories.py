import factory

from provider_service.extra.models import Language, Currency


class LanguageFactory(factory.django.DjangoModelFactory):
    name = factory.Faker("word")

    class Meta:
        model = Language


class CurrencyFactory(factory.django.DjangoModelFactory):
    name = factory.Faker("word")

    class Meta:
        model = Currency
