from django.conf import settings
from django.contrib import admin
from django.urls import include, path, re_path
from rest_framework import permissions

from drf_yasg import openapi
from drf_yasg.views import get_schema_view

schema_view = get_schema_view(
    openapi.Info(
        title='Trading Diary API',
        default_version='v1',
        description='API',
    ),
    public=True,
    permission_classes=(permissions.IsAuthenticated,),
    url=f'{settings.SITE_BASE_URL}',
)

api_v1_urlpatterns = [
    path('', include(('apps.accounting.urls', 'accounting')), name='accounting'),
]

api_urlpatterns = [
    path('docs/', schema_view.with_ui('swagger', cache_timeout=0), name='docs-swagger'),
    re_path(r'^docs(?P<format>\.json|\.yaml)$', schema_view.without_ui(cache_timeout=0), name='schema-json'),
    path('v1/', include((api_v1_urlpatterns, 'v1')), name='v1'),
]

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include(('apps.core.urls', 'core')), name='core'),
    path('api/', include((api_urlpatterns, 'api')), name='api'),
]
