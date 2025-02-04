import datetime

import freezegun
import pytest

from pytest_cases import parametrize_with_cases

from djangology.services import BaseService


@pytest.fixture
def today():
    return datetime.datetime(2022, 1, 1, tzinfo=datetime.timezone.utc)


@pytest.fixture
def tomorrow(today):
    return today + datetime.timedelta(days=1)


class CaseBaseService:
    def request_time__default(self, today):
        return today, {}, today

    def request_time__datetime(self, today, tomorrow):
        return today, {'request_time': tomorrow}, tomorrow


class TestBaseService:
    @parametrize_with_cases(
        ('now', 'kwargs', 'expected'), cases=CaseBaseService, prefix='request_time')
    def test__request_time(self, now, kwargs, expected):
        with freezegun.freeze_time(now):
            service = BaseService(**kwargs)

        assert service.request_time == expected

    def test__kwargs(self):
        service = BaseService(extra_kwarg=True)

        assert service.kwargs == {'extra_kwarg': True}

    def test__context_manager(self):
        with BaseService() as service:
            assert isinstance(service, BaseService)
