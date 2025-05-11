from rest_framework import status

from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema

from apps.accounting.api.serializers.finances import TradingPairSerializer
from apps.accounting.api.serializers.positions import (
    PositionCreateSerializer,
    PositionReadSerializer,
    PositionUpdateSerializer,
)
from apps.accounting.api.viewsets.filters.finances import PositionFilterSet, TradingPairFilterSet
from apps.accounting.models.enums import Exchange, MarketType

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

TRADING_PAIR_TAG = 'TradingPairs'
POSITION_TAG = 'Positions'
POSITION_COMMENT_TAG = 'PositionComments'


class TradingPairViewSetSchema:
    schema = openapi.Schema(
        type=openapi.TYPE_OBJECT,
        description=f'Название бирж, которые доступны в системе. Например: {Exchange._value2member_map_}',
        additional_properties=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            description=f'Название рынка, на котором торгуется актив. Например: {MarketType._value2member_map_}',
            additional_properties=openapi.Schema(
                type=openapi.TYPE_ARRAY,
                items=openapi.Schema(
                    type=openapi.TYPE_OBJECT, ref=f'#/definitions/{TradingPairSerializer.Meta.ref_name}'
                ),
            ),
        ),
    )
    resoponse_200 = openapi.Response(
        description='Список торговых пар.',
        schema=schema,
    )
    retrieve = swagger_auto_schema(
        operation_description='Возвращает информацию о торговой паре.',
        responses={status.HTTP_200_OK: TradingPairSerializer} | COMMON_ERRORS,
        tags=[TRADING_PAIR_TAG],
    )
    list = swagger_auto_schema(
        operation_description='Возвращает список торговых пар, распределенных по биржам и рынкам.',
        responses={status.HTTP_200_OK: resoponse_200} | COMMON_ERRORS,
        tags=[TRADING_PAIR_TAG],
        query_serializer=TradingPairFilterSet.as_serializer(),
    )


class PositionViewSetSchema:
    create = swagger_auto_schema(
        operation_description='Создает позицию.',
        request_body=PositionCreateSerializer,
        responses={status.HTTP_201_CREATED: PositionReadSerializer} | COMMON_ERRORS,
        tags=[POSITION_TAG],
    )
    partial_update = swagger_auto_schema(
        operation_description='Обновляет позицию.',
        request_body=PositionUpdateSerializer,
        responses={status.HTTP_200_OK: PositionReadSerializer} | COMMON_ERRORS,
        tags=[POSITION_TAG],
    )
    retrieve = swagger_auto_schema(
        operation_description='Возвращает информацию о позиции.',
        responses={status.HTTP_200_OK: PositionReadSerializer} | COMMON_ERRORS,
        tags=[POSITION_TAG],
    )
    list = swagger_auto_schema(
        operation_description='Возвращает список позиций.',
        responses=COMMON_ERRORS,
        tags=[POSITION_TAG],
        query_serializer=PositionFilterSet.as_serializer(),
    )
    destroy = swagger_auto_schema(
        operation_description='Удаляет позицию.',
        responses=COMMON_ERRORS,
        tags=[POSITION_TAG],
    )


class PositionCommentViewSetSchema:
    create = swagger_auto_schema(
        operation_description='Создает комментарий к позиции.',
        responses=COMMON_ERRORS,
        tags=[POSITION_COMMENT_TAG],
    )
    partial_update = swagger_auto_schema(
        operation_description='Обновляет комментарий к позиции.',
        responses=COMMON_ERRORS,
        tags=[POSITION_COMMENT_TAG],
    )
    destroy = swagger_auto_schema(
        operation_description='Удаляет комментарий к позиции.',
        responses=COMMON_ERRORS,
        tags=[POSITION_COMMENT_TAG],
    )
