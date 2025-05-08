from django import forms
from django.contrib import admin
from django.forms import PasswordInput

from apps.bybit.models import ByBitAccess


class ByBitAccessForm(forms.ModelForm):
    class Meta:
        model = ByBitAccess
        fields = (
            'key',
            'secret',
            'is_active',
        )
        widgets = {
            'key': PasswordInput(render_value=True),
            'secret': PasswordInput(render_value=True),
        }


class ByBitAccessInline(admin.StackedInline):
    model = ByBitAccess
    form = ByBitAccessForm
    fieldsets = (
        (
            'Данные доступа',
            {
                'fields': (
                    'key',
                    'secret',
                    'is_active',
                ),
            },
        ),
        (
            'Даты',
            {
                'fields': (
                    'created_at',
                    'modified_at',
                ),
                'classes': ('collapse',),
            },
        ),
    )
    readonly_fields = ('created_at', 'modified_at')
    verbose_name = 'Доступ к ByBit'
    verbose_name_plural = 'Доступы к ByBit'
