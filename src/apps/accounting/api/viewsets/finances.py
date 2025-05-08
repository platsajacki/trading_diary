from django.utils.decorators import method_decorator

from rest_framework.generics import ListAPIView
from rest_framework.permissions import IsAuthenticated

from apps.accounting.api.schemas import TradingPairListAPIViewSchema
from apps.accounting.api.serializers.finances import TradingPairSerializer
from apps.accounting.api.viewsets.filters import TradingPairFilterSet
from apps.accounting.models import TradingPair


@method_decorator(name='get', decorator=TradingPairListAPIViewSchema.get)
class TradingPairListAPIView(ListAPIView):
    serializer_class = TradingPairSerializer
    queryset = TradingPair.objects.with_select_related()
    permission_classes = [IsAuthenticated]
    filterset_class = TradingPairFilterSet
