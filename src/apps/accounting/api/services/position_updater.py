from rest_framework import status
from rest_framework.response import Response

from apps.accounting.api.serializers.positions import PositionReadSerializer, PositionUpdateSerializer
from apps.core.services.interfaces import ViewSetService


class PositionUpdater(ViewSetService):
    def act(self) -> Response:
        instance = self.viewset.get_object()
        serializer = PositionUpdateSerializer(instance, data=self.request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        position = serializer.save()
        return Response(PositionReadSerializer(position).data, status=status.HTTP_200_OK)
