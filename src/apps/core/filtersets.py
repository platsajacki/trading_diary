from typing import Any

from django_filters import rest_framework as filters
from rest_framework import serializers


class FilterSet(filters.FilterSet):

    class Meta:
        abstract = True

    @classmethod
    def as_serializer(cls) -> type[serializers.Serializer]:
        """
        Возвращает сериализатор, описывающий поля фильтра для использования в Swagger.
        """
        fields = {}
        for name, filter_field in cls.base_filters.items():
            serializer_field_class: Any = serializers.CharField
            if hasattr(filter_field, 'field'):
                django_field = filter_field.field
                if isinstance(django_field, (filters.BooleanFilter.field_class,)):
                    serializer_field_class = serializers.BooleanField
                elif isinstance(django_field, (filters.NumberFilter.field_class,)):
                    serializer_field_class = serializers.FloatField
                elif isinstance(django_field, filters.DateFilter.field_class):
                    serializer_field_class = serializers.DateField
            fields[name] = serializer_field_class(required=False)
        return type(f'{cls.__name__}SwaggerSerializer', (serializers.Serializer,), fields)
