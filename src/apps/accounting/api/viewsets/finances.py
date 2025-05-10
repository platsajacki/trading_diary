from django.utils.decorators import method_decorator
from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import ModelViewSet

from apps.accounting.api.schemas import TradingPairListAPIViewSchema
from apps.accounting.api.serializers.finances import TradingPairSerializer
from apps.accounting.api.viewsets.filters import TradingPairFilterSet
from apps.accounting.models import TradingPair


@method_decorator(name='list', decorator=TradingPairListAPIViewSchema.list)
@method_decorator(name='retrieve', decorator=TradingPairListAPIViewSchema.retrieve)
class TradingPairListAPIView(ModelViewSet):
    serializer_class = TradingPairSerializer
    queryset = TradingPair.objects.with_select_related()
    permission_classes = [IsAuthenticated]
    filterset_class = TradingPairFilterSet
    http_method_names = ['get']
