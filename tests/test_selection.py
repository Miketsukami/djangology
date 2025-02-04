import pytest

from pytest_cases import parametrize_with_cases, case
from pytest_unordered import unordered

from djangology.selection import BaseModelSelection
from djangology.selection.exceptions import ObjectNotFoundError, ObjectNotUniqueError

from .dummy.models import Dummy


class DummySelection(BaseModelSelection):
    model = Dummy


@pytest.fixture()
def dummies(dummy_factory):
    return [
        dummy_factory(value=1),
        dummy_factory(value=2),
        dummy_factory(value=2),
    ]


class CaseBaseModelSelection:
    def queryset__default(self, dummies):
        return None, unordered(dummies)

    def queryset__custom(self, dummies):
        return Dummy.objects.filter(value__gt=dummies[0].value), unordered(dummies[1:])

    def pks__default(self, dummies):
        return None, unordered([d.pk for d in dummies])

    def pks__custom(self, dummies):
        first, *others = dummies
        return Dummy.objects.filter(value__gt=first.value), unordered([d.pk for d in others])

    @case(tags='default')
    def get_object__found(self, dummies):
        return dummies[0].value, dummies[0]

    @case(tags='default')
    def get_object__none(self):
        return 0, None

    @case(tags='exception')
    def get_object__exception_not_unique(self, dummies):
        return dummies[1].value, ObjectNotUniqueError

    @case(tags='exception')
    def get_object__exception_not_found(self):
        return 0, ObjectNotFoundError


@pytest.mark.django_db
class TestBaseModelSelection:
    @parametrize_with_cases(
        ('queryset', 'expected'), cases=CaseBaseModelSelection, prefix='queryset')
    def test__queryset(self, queryset, expected):
        selector = DummySelection(queryset=queryset)

        assert list(selector.queryset) == expected

    @parametrize_with_cases(
        ('queryset', 'expected'), cases=CaseBaseModelSelection, prefix='pks')
    def test__pks(self, queryset, expected):
        selector = DummySelection(queryset=queryset)

        assert selector.pks == expected

    @parametrize_with_cases(
        ('value', 'expected'), cases=CaseBaseModelSelection, prefix='get_object', has_tag='default')
    def test__get_object__default(self, value, expected):
        dummy = DummySelection().get_object(value=value, raise_exception=False)

        assert dummy == expected

    @parametrize_with_cases(
        ('value', 'exception'), cases=CaseBaseModelSelection, prefix='get_object', has_tag='exception')
    def test__get_object__exception(self, value, exception):
        with pytest.raises(exception):
            DummySelection().get_object(value=value, raise_exception=True)
