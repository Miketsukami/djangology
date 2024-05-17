from __future__ import annotations

import abc
import typing

from django.core.exceptions import MultipleObjectsReturned, ObjectDoesNotExist

from .types import TModel


if typing.TYPE_CHECKING:
    from django.db.models import QuerySet


class BaseModelSelector(typing.Generic[TModel], abc.ABC):
    model: type[TModel]

    @typing.final
    def __init__(self, queryset: QuerySet[TModel] | None = None) -> None:
        if queryset is None:
            queryset = self.model.objects.all()

        self.queryset = queryset

    @typing.final
    def select_related(self, *lookups: str) -> typing.Self:
        self.queryset = self.queryset.select_related(*lookups)
        return self

    @typing.final
    def get_queryset(self) -> QuerySet[TModel]:
        return self.queryset

    @typing.final
    def get_object(self, **params: typing.Any) -> TModel | None:
        try:
            return self.queryset.get(**params)
        except (ObjectDoesNotExist, MultipleObjectsReturned):
            pass

    @typing.final
    @property
    def pks(self) -> list[int]:
        return list(self.queryset.values_list('pk', flat=True))