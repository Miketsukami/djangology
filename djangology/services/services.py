from __future__ import annotations

import datetime
import types
import typing

from django.utils import timezone


class BaseService:
    def __init__(self, *, request_time: datetime.datetime | None = None, **kwargs: typing.Any) -> None:
        self.request_time = request_time
        if request_time is None:
            self.request_time = timezone.now()

        self.kwargs = kwargs

    @typing.final
    def __enter__(self) -> typing.Self:
        return self

    @typing.final
    def __exit__(
        self, exc_type: type[BaseException] | None, exc_val: BaseException | None, exc_tb: types.TracebackType | None
    ) -> None:
        pass
