from django.urls import path

from apps.settings.views import InstallTypeListAPIView, InstallTypeCreateAPIView, InstallTypeUpdateAPIView

urlpatterns = [
	path('install-type-create/', InstallTypeCreateAPIView.as_view(), name="install_type_create"),
	path('install-type-list/', InstallTypeListAPIView.as_view(), name="install_type_list"),
	path('install-type-update/<int:pk>/', InstallTypeUpdateAPIView.as_view(), name="install_type_update"),
]

