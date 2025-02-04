from ..exceptions import DjangologyError


class SelectionError(DjangologyError):
    pass


class ObjectNotFoundError(SelectionError):
    pass


class ObjectNotUniqueError(SelectionError):
    pass
