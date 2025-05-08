from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status

from apps.accounting.api.serializers.finances import TradingPairSerializer
from apps.accounting.api.viewsets.filters.finances import TradingPairFilterSet

ERROR_403 = openapi.Schema(
    type=openapi.TYPE_OBJECT,
    properties={'detail': openapi.Schema(type=openapi.TYPE_STRING, example='Forbidden.')},
    required=['detail'],
    description='403 Forbidden error. The server understood the request, but it refuses to authorize it.',
)
ERROR_401 = openapi.Schema(
    type=openapi.TYPE_OBJECT,
    properties={'detail': openapi.Schema(type=openapi.TYPE_STRING, example='Unauthorized.')},
    required=['detail'],
    description=(
        '401 Unauthorized error. '
        'The request has not been applied because it lacks valid authentication credentials for the target resource.',
    ),
)
ERROR_400 = openapi.Schema(
    type=openapi.TYPE_OBJECT,
    properties={'detail': openapi.Schema(type=openapi.TYPE_STRING, example='Bad Request.')},
    required=['detail'],
    description=(
        '400 Bad Request error. ' 'The server cannot or will not process the request due to an apparent client error.',
    ),
)
ERROR_404 = openapi.Schema(
    type=openapi.TYPE_OBJECT,
    properties={'detail': openapi.Schema(type=openapi.TYPE_STRING, example='Not Found.')},
    required=['detail'],
    description='404 Not Found error. The server can not find the requested resource.',
)

COMMON_ERRORS = {
    status.HTTP_400_BAD_REQUEST: ERROR_400,
    status.HTTP_401_UNAUTHORIZED: ERROR_401,
    status.HTTP_403_FORBIDDEN: ERROR_403,
    status.HTTP_404_NOT_FOUND: ERROR_404,
}

TRADING_PAIR_TAG = 'TradingPair'


class TradingPairListAPIViewSchema:
    get = swagger_auto_schema(
        operation_description='Возвращает список торговых пар.',
        responses={status.HTTP_200_OK: TradingPairSerializer} | COMMON_ERRORS,
        tags=[TRADING_PAIR_TAG],
        query_serializer=TradingPairFilterSet.as_serializer(),
    )
