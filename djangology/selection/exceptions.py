import deprecation

from djangology import __version__
from djangology.selectors.exceptions import (
    SelectorError,
    ObjectNotFoundError as _ObjectNotFoundError,
    ObjectNotUniqueError as _ObjectNotUniqueError
)


@deprecation.deprecated(deprecated_in='0.1.4', removed_in='0.2', current_version=__version__)
class SelectionError(SelectorError):
    pass


@deprecation.deprecated(deprecated_in='0.1.4', removed_in='0.2', current_version=__version__)
class ObjectNotFoundError(SelectionError, _ObjectNotFoundError):
    pass


@deprecation.deprecated(deprecated_in='0.1.4', removed_in='0.2', current_version=__version__)
class ObjectNotUniqueError(SelectionError, _ObjectNotUniqueError):
    pass
