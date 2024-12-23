"""
URL configuration for notebook_project project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf import settings
from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from accounts.views import ResetPasswordAPIView, ResetPasswordConfirmAPIView
from notes.views import home_view

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', home_view, name='home'), 
    path('api/accounts/', include('accounts.urls')),
    path('api/notes/', include('notes.urls')),  # Маршруты заметок
    # path('password_reset/', include('django.contrib.auth.urls')),  # Встроенные маршруты для сброса пароля
    # path('reset-password/<uidb64>/<token>/', ResetPasswordAPIView.as_view(), name='password_reset_confirm'),
    # in your Django urls.py
    # path('reset-password/<uidb64>/<token>/', ResetPasswordConfirmAPIView.as_view(), name='reset-password-confirm'),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
