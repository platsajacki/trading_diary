from django.db import models

from encrypted_fields.fields import EncryptedCharField


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


class KeyFieldModel(models.Model):
    key = EncryptedCharField(
        'API ключ',
        max_length=512,
        help_text='API ключ для доступа к внешнему сервису',
    )

    class Meta:
        abstract = True


class SecretFieldModel(models.Model):
    secret = EncryptedCharField(
        'API секрет',
        max_length=255,
        help_text='API секрет для доступа к внешнему сервису',
    )

    class Meta:
        abstract = True


class KeySecretFieldModel(SecretFieldModel, KeyFieldModel):
    is_active = models.BooleanField(
        'Активен',
        default=True,
        help_text='Флаг, указывающий, активен ли доступ к API',
    )

    class Meta:
        abstract = True
