from django.contrib import admin
from django.urls import path, include
from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from rest_framework import permissions
from django.urls import path, include

schema_view = get_schema_view(
    openapi.Info(
        title="Support",
        default_version='v1',
        description="Support service on Django Rest Framework",
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)

urlpatterns = [
    path('docs/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('admin/', admin.site.urls),
    path('auth/', include('profiles.urls')),
    path('', include('tikets.urls'))
]
