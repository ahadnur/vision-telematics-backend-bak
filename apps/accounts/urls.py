from django.urls import path
from apps.accounts.views import (activate, CreateAccountAPIView, UpdateAccountAPIView, UserCreateAPIView,
                                 ResetUserPasswordAPIView, GetUserAPIView, AccountListAPIView, LoginAPIView,
                                 UserListAPIView, UserUpdateAPIView, AccountDropdownListAPIView, GetAccountAPIView,
                                 CompanyCreateAPIView, CompanyUpdateAPIView, CompanyListAPIView, CompanyRetrieveAPIView,
                                 CompanyDestroyAPIView)


urlpatterns = [
    path('activate/<uid64>/<token>/', activate, name='activate'),
]+[
    path('user_list/', UserListAPIView.as_view(), name='user_list'),
    path('user/<_id>/', GetUserAPIView.as_view(), name='user'),
    path('user-create/', UserCreateAPIView.as_view(), name='user_create'),
    path('user-update/<pk>/', UserUpdateAPIView.as_view(), name='user_update'),
    path('login/', LoginAPIView.as_view(), name='user_login'),
    # path('user/reset-password/<_id>/', ResetUserPasswordAPIView.as_view(), name='reset-password'),
]+[
    path('create/', CreateAccountAPIView.as_view(), name='account_create'),
    path('update/<int:_id>/', UpdateAccountAPIView.as_view(), name='account_update'),
    path('detail/<int:pk>/', GetAccountAPIView.as_view(), name='get_account'),
    path('account-list/', AccountListAPIView.as_view(), name='account_list'),
    path('account-list-dropdown/', AccountDropdownListAPIView.as_view(), name='account_list_dropdown'),
] + [
    path('company-create/', CompanyCreateAPIView.as_view(), name='company_create'),
    path('company-update/<int:pk>/', CompanyUpdateAPIView.as_view(), name='company_update'),
    path('company-list/', CompanyListAPIView.as_view(), name='company_list'),
    path('company-retrieve/<int:pk>/', CompanyRetrieveAPIView.as_view(), name='company_retrieve'),
    path('company-delete/<int:pk>/', CompanyDestroyAPIView.as_view(), name='company_delete'),
]
