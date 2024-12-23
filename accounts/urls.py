from django.urls import path
from .views import LoginAPIView, LogoutAPIView, RegisterAPIView, ResetPasswordAPIView,CurrentUserAPIView, ResetPasswordConfirmAPIView

urlpatterns = [
    path('register/', RegisterAPIView.as_view(), name='accounts_register'),
    path('login/', LoginAPIView.as_view(), name='accounts_login'),
    path('logout/', LogoutAPIView.as_view(), name='accounts_logout'),
    path('reset-password/', ResetPasswordAPIView.as_view(), name='password_reset_request'),  # For email submission
    path('reset-password/<uidb64>/<token>/', ResetPasswordConfirmAPIView.as_view(), name='password_reset_confirm'),  # For resetting password
    path('current-user/', CurrentUserAPIView.as_view(), name='current-user'),
]
