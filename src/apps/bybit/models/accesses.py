from django.db import models

from apps.core.models import KeySecretFieldModel, TimestampedModel
from apps.users.models import User


class ByBitAccess(TimestampedModel, KeySecretFieldModel):
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name='bybit_access',
        verbose_name='Пользователь',
    )

    class Meta:
        verbose_name = 'Доступ к ByBit'
        verbose_name_plural = 'Доступы к ByBit'

    def __str__(self) -> str:
        return f'{self._meta.verbose_name} пользователя {self.user.username}'

    def __repr__(self) -> str:
        return f'{self.__class__.__name__}({self.key.__name__}, {self.secret.__name__}, {self.user})'
