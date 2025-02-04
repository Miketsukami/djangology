import typing

from django.db.models.base import Model


TModel = typing.TypeVar('TModel', bound=Model)
