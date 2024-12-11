from django.urls import path
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
from .views import login_view, logout_view, register_view, reset_password_view, token_view

urlpatterns = [
    path('register/', register_view, name='register_form'),
    path('login/', login_view, name='login_form'),
    path('reset-password/', reset_password_view, name='reset_password_form'),
    path('tokens/', token_view, name='tokens'),
    path('logout/', logout_view, name='logout'), 
]