from dataclasses import dataclass
from typing import Any

from django.db.models import Model
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.serializers import BaseSerializer
from rest_framework.viewsets import ModelViewSet

from apps.core.exceptions import NotImplementedMethodError
from apps.core.services.base import BaseService, DataFetcherService, DataProcessorService, DataSaverService


class DataPipelineService(DataFetcherService, DataProcessorService, DataSaverService):
    """
    Сервис для полного цикла обработки данных: извлечение, обработка и сохранение в базу данных.

    Этот класс объединяет три этапа работы с данными: извлечение данных из внешнего источника,
    их обработку и запись в базу данных. Конкретная реализация этого класса должна предоставить
    механизм для выполнения всех этапов.

    Методы:
        act() -> Any:
            Метод для выполнения основной логики сервиса, включающей извлечение, обработку и
            сохранение данных. Должен быть реализован в дочерних классах.
        __call__() -> Any:
            Вызывает основной метод `act()`, обеспечивая возможность использования экземпляра сервиса как функции.
        fetch_data() -> Any:
            Метод для извлечения данных из внешнего источника. Должен быть реализован в дочерних классах.
        process_data(data: Any) -> Any:
            Метод для обработки извлечённых данных. Должен быть реализован в дочерних классах.
        save_to_database(processed_data: Any) -> None:
            Метод для записи обработанных данных в базу данных. Должен быть реализован в дочерних классах.

    Исключения:
        NotImplementedError:
            Если любой из методов `fetch_data`, `process_data`, `save_to_database` или `act` не реализован
            в дочернем классе, будет вызвано это исключение.
    """

    def act(self) -> Any:
        """
        Выполняет полный процесс обработки данных: извлечение, обработка и сохранение.

        Этот метод последовательно вызывает `fetch_data` для получения данных, `process_data` для
        их обработки и `save_to_database` для записи обработанных данных в базу данных.

        Возвращает:
            Any: Результат выполнения логики сервиса. Можно возвращать результаты, статус выполнения или `None`.
        """
        data = self.fetch_data()
        processed_data = self.process_data(data)
        self.save_to_database(processed_data)
        return processed_data


@dataclass
class ViewSetService(BaseService):
    """
    Сервис для обработки данных в контексте ViewSet.

    Этот класс расширяет функциональность `BaseService`, добавляя возможность
    работы с запросами и ответами в контексте Django REST Framework.

    Атрибуты:
        request (Request): Запрос, полученный от клиента.
        viewset (ModelViewSet): ViewSet, с которым связан данный сервис.

    Методы:
        act() -> Response:
            Выполняет основную логику обработки данных в контексте ViewSet. Отдает ответ клиенту.
        __call__() -> Response:
            Вызывает основной метод `act()`, обеспечивая возможность использования
            экземпляра сервиса как функции.
    """

    request: Request
    viewset: ModelViewSet

    def get_validated_data(self) -> dict[str, Any]:
        """
        Получает валидированные данные из запроса.

        Этот метод извлекает валидированные данные из запроса, используя сериализатор
        ViewSet. Если сериализатор не валиден, будет вызвано исключение.

        Возвращает:
            dict[str, Any]: Валидированные данные из запроса.
        """
        serializer = self.get_serializer()
        return serializer.validated_data

    def get_serializer(self, instance: Model | None = None, partial: bool = False) -> BaseSerializer:
        """
        Получает сериализатор для обработки данных.
        Этот метод создает экземпляр сериализатора, используя данные из запроса.
        Если передан экземпляр модели, он будет использоваться для инициализации сериализатора.
        Параметры:
            instance (Model | None): Экземпляр модели для инициализации сериализатора.
            partial (bool): Флаг, указывающий, является ли обновление частичным.
        Возвращает:
            BaseSerializer: Экземпляр сериализатора, готовый к валидации и сохранению данных.
        """
        serializer = self.viewset.get_serializer(instance, data=self.request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        return serializer

    def act(self) -> Response:
        """
        Выполняет основную логику обработки данных в контексте ViewSet.

        Этот метод должен быть реализован в дочерних классах и должен возвращать
        ответ клиенту.

        Возвращает:
            Response: Ответ, который будет отправлен клиенту.
        """
        raise NotImplementedMethodError(self.__class__.__name__, self.act.__name__)
