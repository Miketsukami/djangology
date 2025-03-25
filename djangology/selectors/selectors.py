import abc
import typing

from contextlib import AbstractContextManager
from types import TracebackType

from django.core.exceptions import ObjectDoesNotExist, MultipleObjectsReturned
from django.db.models.query import QuerySet

import deprecation

from djangology import __version__

from .exceptions import ObjectNotFoundError, ObjectNotUniqueError
from .types import TModel


class BaseModelSelector(typing.Generic[TModel], AbstractContextManager, abc.ABC):
    model: type[TModel]
    queryset: QuerySet[TModel]

    def __init__(self, queryset: QuerySet[TModel] | None = None) -> None:
        if queryset is None:
            queryset = self.model.objects.all()

        self.queryset = queryset

    def __exit__(
        self, exc_type: type[BaseException], exc_value: BaseException | None, traceback: TracebackType | None
    ) -> None:
        pass

    @property
    def pks(self) -> list[typing.Any]:
        return list(self.queryset.values_list('pk', flat=True))

    @deprecation.deprecated(deprecated_in='0.1.4', removed_in='2.0', current_version=__version__)
    def order_by(self, *lookups: str) -> typing.Self:
        self.queryset = self.queryset.order_by(*lookups)

        return self

    def get_object(self, *, raise_exception: bool = True, **params: typing.Any) -> TModel | None:
        try:
            return self.queryset.get(**params)
        except ObjectDoesNotExist as e:
            if raise_exception:
                raise ObjectNotFoundError from e
        except MultipleObjectsReturned as e:
            raise ObjectNotUniqueError from e
