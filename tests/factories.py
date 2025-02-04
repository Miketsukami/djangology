import factory

from factory import fuzzy


class DummyFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = 'dummy.Dummy'

    value = fuzzy.FuzzyInteger(low=0, high=100)
