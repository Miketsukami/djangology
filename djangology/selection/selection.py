from __future__ import annotations

import abc

import deprecation

from djangology import __version__
from djangology.selectors import BaseModelSelector

from .types import TModel


@deprecation.deprecated(
    deprecated_in='0.1.4', removed_in='0.2', current_version=__version__, details='Use `selectors.BaseModelSelector`'
)
class BaseModelSelection(BaseModelSelector[TModel], abc.ABC):
    pass
