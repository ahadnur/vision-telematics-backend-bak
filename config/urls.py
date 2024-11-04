from django.contrib import admin
from django.conf import settings
from django.urls import path, include
from django.shortcuts import redirect
from rest_framework import permissions
from rest_framework.authentication import SessionAuthentication
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from .authentication import JWTAuthentication


admin.site.site_header = 'Vision Telematics'

swagger_url_patterns = None
if settings.DEBUG:
    schema_view = get_schema_view(
        openapi.Info(
            title="Your API",
            default_version='v1',
            description="API description",
            terms_of_service="https://www.yourapp.com/terms/",
            contact=openapi.Contact(email="contact@yourapp.com"),
            license=openapi.License(name="Your License"),
        ),
        public=True,
        permission_classes=[permissions.AllowAny, ],
        authentication_classes=[SessionAuthentication, JWTAuthentication],
    )
    swagger_url_patterns = [
        path('', lambda request: redirect('/swagger/', permanent=True)),
        path('swagger<str:format>', schema_view.without_ui(cache_timeout=0), name='schema-json'),
        path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
        path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
    ]

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/account/', include('apps.accounts.urls')),
    path('api/customers/', include('apps.customers.urls')),
    path('api/engineers/', include('apps.engineers.urls')),
    path('api/products/', include('apps.products.urls')),
    path('api/orders/', include('apps.orders.urls')),
    path('api/settings/', include('apps.settings.urls')),
    # path()
]

if settings.DEBUG and swagger_url_patterns:
    urlpatterns += swagger_url_patterns
