from django.urls import path
from .views import activate, CreateAccountAPIView, UpdateAccountAPIView

app_name = 'accounts'

urlpatterns = [
    path('activate/<uid64>/<token>/', activate, name='activate'),
]+[
    path('user-create/', CreateAccountAPIView.as_view(), name='user-create'),
]+[
    path('create-new-account/', CreateAccountAPIView.as_view(), name='create-account'),
    path('update-new-account/<int:id>/', UpdateAccountAPIView.as_view(), name='update-account'),
]