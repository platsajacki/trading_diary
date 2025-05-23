# Generated by Django 5.2 on 2025-05-07 11:46

import django.db.models.deletion
import encrypted_fields.fields
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='ByBitAccess',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Дата и время создания')),
                ('modified_at', models.DateTimeField(auto_now=True, verbose_name='Дата и время изменения')),
                (
                    'key',
                    encrypted_fields.fields.EncryptedCharField(
                        help_text='API ключ для доступа к внешнему сервису', max_length=512, verbose_name='API ключ'
                    ),
                ),
                (
                    'secret',
                    encrypted_fields.fields.EncryptedCharField(
                        help_text='API секрет для доступа к внешнему сервису', max_length=255, verbose_name='API секрет'
                    ),
                ),
                (
                    'is_active',
                    models.BooleanField(
                        default=True, help_text='Флаг, указывающий, активен ли доступ к API', verbose_name='Активен'
                    ),
                ),
                (
                    'user',
                    models.OneToOneField(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name='bybit_access',
                        to=settings.AUTH_USER_MODEL,
                        verbose_name='Пользователь',
                    ),
                ),
            ],
            options={
                'verbose_name': 'Доступ к ByBit',
                'verbose_name_plural': 'Доступы к ByBit',
            },
        ),
    ]
