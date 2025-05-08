from accounting.api.serializers.finances import TradingPairSerializer
from accounting.models import TradingPair
from rest_framework.generics import ListAPIView
from rest_framework.permissions import IsAuthenticated


class TradingPairListAPIView(ListAPIView):
    serializer_class = TradingPairSerializer
    queryset = TradingPair.objects.with_select_related()
    permission_classes = [IsAuthenticated]
