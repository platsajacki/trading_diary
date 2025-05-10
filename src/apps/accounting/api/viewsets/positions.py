# from django.utils.decorators import method_decorator
from typing import Any

from rest_framework.exceptions import MethodNotAllowed
from rest_framework.permissions import IsAuthenticated
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.serializers import Serializer
from rest_framework.viewsets import ModelViewSet

from apps.accounting.api.serializers.positions import (
    PositionCreateSerializer,
    PositionReadSerializer,
    PositionUpdateSerializer,
)
from apps.accounting.api.services.position_creator import PositionCreator
from apps.accounting.api.services.position_updater import PositionUpdater
from apps.accounting.api.viewsets.filters import PositionFilterSet
from apps.accounting.models import Position
from apps.core.paginators import PageNumberPagination


class PositionViewSet(ModelViewSet):
    serializer_class = PositionReadSerializer
    queryset = Position.objects.with_select_related()
    permission_classes = [IsAuthenticated]
    filterset_class = PositionFilterSet
    pagination_class = PageNumberPagination
    http_method_names = ['get', 'post', 'patch', 'delete']

    def get_serializer_class(self) -> type[Serializer]:
        if self.action == 'create':
            return PositionCreateSerializer
        if self.action == 'partial_update':
            return PositionUpdateSerializer
        if self.action == 'update':
            raise MethodNotAllowed('PUT', detail='Use PATCH instead of PUT for update.')
        return PositionReadSerializer

    def create(self, request: Request, *args: Any, **kwargs: Any) -> Response:
        return PositionCreator(request, self)()

    def partial_update(self, request: Request, *args: Any, **kwargs: Any) -> Response:
        return PositionUpdater(request, self)()
