from typing import Any, Callable, Optional, Type, TypeVar

from django.utils.decorators import method_decorator

T = TypeVar('T', bound=type)

VIEWSET_METHODS = [
    'create',
    'retrieve',
    'update',
    'partial_update',
    'destroy',
    'list',
]


def apply_viewset_schema(schema_cls: Type[Any]) -> Callable[[T], T]:
    def decorator(view_cls: T) -> T:
        for method_name in VIEWSET_METHODS:
            schema_method: Optional[Callable[..., Any]] = getattr(schema_cls, method_name, None)
            if schema_method:
                original: Callable[..., Any] = getattr(view_cls, method_name)
                decorated = method_decorator(schema_method)(original)
                setattr(view_cls, method_name, decorated)
        return view_cls

    return decorator
