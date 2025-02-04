from django.db import models


class Dummy(models.Model):
    value = models.IntegerField()

    class Meta:
        verbose_name = 'Dummy'
        verbose_name_plural = 'Dummy'

    def __str__(self) -> str:  # pragma: nocover
        return self.pk
