from django.urls import path
from apps.utilities.views import *

urlpatterns = [
	path('vehicle-type-create/', VehicleTypeCreateAPIView.as_view(), name='vehicle_type_create'),
	path('vehicle-type-list/', VehicleTypeListAPIView.as_view(), name='vehicle_type_list'),
	path('vehicle-type-detail/<pk>/', VehicleTypeRetrieveAPIView.as_view(), name='vehicle_type_detail'),
	path('vehicle-type-update/<pk>/', VehicleTypeUpdateAPIView.as_view(), name='vehicle_type_update'),
	path('vehicle-type-delete/<pk>/', VehicleTypeDeleteAPIView.as_view(), name='vehicle_type_delete'),
] + [
	path('vehicle-make-create/', VehicleMakeCreateAPIView.as_view(), name='vehicle_make_create'),
	path('vehicle-make-list/', VehicleMakeListAPIView.as_view(), name='vehicle_make_list'),
	path('vehicle-make-detail/<pk>/', VehicleMakeRetrieveAPIView.as_view(), name='vehicle_make_detail'),
	path('vehicle-make-update/<pk>/', VehicleMakeUpdateAPIView.as_view(), name='vehicle_make_update'),
	path('vehicle-make-delete/<pk>/', VehicleMakeDeleteAPIView.as_view(), name='vehicle_make_delete'),
] + [
	path('vehicle-model-create/', VehicleModelCreateAPIView.as_view(), name='vehicle_model_create'),
	path('vehicle-model-list/', VehicleModelListAPIView.as_view(), name='vehicle_model_list'),
	path('vehicle-model-detail/<pk>/', VehicleModelRetrieveAPIView.as_view(), name='vehicle_model_detail'),
	path('vehicle-model-update/<pk>/', VehicleModelUpdateAPIView.as_view(), name='vehicle_model_update'),
	path('vehicle-model-delete/<pk>/', VehicleModelDeleteAPIView.as_view(), name='vehicle_model_delete'),
]
