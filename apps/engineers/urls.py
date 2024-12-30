from django.urls import path
from apps.engineers.views import (EngineerCompanyListAPIView, EngineerCreateAPIView, EngineerListAPIView,
                                  EngineerRetrieveAPIView, EngineerUpdateAPIView, EngineerDestroyAPIView)

app_name = 'engineers'

urlpatterns = [
    path('company-list/', EngineerCompanyListAPIView.as_view(), name='company-list'),
    path('list/', EngineerListAPIView.as_view(), name='engineer-list'),
    path('create/', EngineerCreateAPIView.as_view(), name='create-engineer'),
    path('detail/<int:pk>/', EngineerRetrieveAPIView.as_view(), name='get-engineer'),
    path('update/<int:pk>/', EngineerUpdateAPIView.as_view(), name='update-engineer'),
    path('delete/<pk>/', EngineerDestroyAPIView.as_view(), name='delete-engineer'),
]
