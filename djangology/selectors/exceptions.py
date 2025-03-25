from djangology.exceptions import DjangologyError


class SelectorError(DjangologyError):
    pass


class ObjectNotFoundError(SelectorError):
    pass


class ObjectNotUniqueError(SelectorError):
    pass
