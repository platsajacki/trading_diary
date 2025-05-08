from django.conf import settings
from django.contrib import admin
from django.urls import include, path, re_path

from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from rest_framework import permissions

schema_view = get_schema_view(
    openapi.Info(
        title='Trading Diary API',
        default_version='v1',
        description='API',
    ),
    public=True,
    permission_classes=(permissions.IsAuthenticated,),
    url=f'{settings.SITE_BASE_URL}api',
)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/v1/docs/', schema_view.with_ui('swagger', cache_timeout=0), name='docs-swagger'),
    re_path(r'^api/v1/docs(?P<format>\.json|\.yaml)$', schema_view.without_ui(cache_timeout=0), name='schema-json'),
    path('api/v1/', include('accounting.urls')),
]
