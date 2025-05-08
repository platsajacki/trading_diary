from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as DjangoUserAdmin
from django.db.models import QuerySet
from django.http import HttpRequest

from apps.bybit.admin import ByBitAccessInline
from apps.users.models import User


@admin.register(User)
class UserAdmin(DjangoUserAdmin):
    inlines = [ByBitAccessInline]

    def get_queryset(self, request: HttpRequest) -> QuerySet[User]:
        return super().get_queryset(request).select_related('bybit_access')
