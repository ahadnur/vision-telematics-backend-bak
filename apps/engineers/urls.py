from django.urls import path
from apps.engineers.views import (EngineerCompanyListAPIView, EngineerCreateAPIView, EngineerListAPIView,
                                  EngineerRetrieveAPIView, EngineerUpdateAPIView,)

app_name = 'engineers'

urlpatterns = [
    path('company-list/', EngineerCompanyListAPIView.as_view(), name='company-list'),
    path('engineer-list/', EngineerListAPIView.as_view(), name='engineer-list'),
    path('engineer-create/', EngineerCreateAPIView.as_view(), name='create-engineer'),
    path('engineer/<pk>/', EngineerRetrieveAPIView.as_view(), name='get-engineer'),
    path('engineer/<pk>/', EngineerUpdateAPIView.as_view(), name='update-engineer'),
]
