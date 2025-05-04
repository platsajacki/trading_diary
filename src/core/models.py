from django.db import models


class NameStringMethod(models.Model):
    class Meta:
        abstract = True

    def __str__(self) -> str:
        name = getattr(self, 'name', None)
        if name is not None:
            return str(name)
        return super().__str__()


class TimestampedModel(models.Model):
    created_at = models.DateTimeField(
        'Дата и время создания',
        auto_now_add=True,
    )
    modified_at = models.DateTimeField(
        'Дата и время изменения',
        auto_now=True,
    )

    class Meta:
        abstract = True
