from django.shortcuts import render

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import RegisterSerializer
from rest_framework_simplejwt.tokens import RefreshToken
from django.core.mail import send_mail
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.contrib.auth import get_user_model
from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from django.contrib.auth import logout



User = get_user_model()

def register_view(request):
    if request.method == "POST":
        serializer = RegisterSerializer(data=request.POST)
        if serializer.is_valid():
            user = serializer.save()
            login(request, user)  # Логиним пользователя после регистрации
            return redirect('login_form')  # Перенаправляем на главную страницу
        return render(request, 'accounts/register.html', {'errors': serializer.errors})
    return render(request, 'accounts/register.html')

def login_view(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            return redirect('home')  # Перенаправляем на главную страницу
        return render(request, 'accounts/login.html', {'error': 'Invalid credentials'})
    return render(request, 'accounts/login.html')


def logout_view(request):
    logout(request)  # Удаляем данные текущей сессии пользователя
    return redirect('home')  # Перенаправляем на главную страницу


def reset_password_view(request):
    if request.method == "POST":
        email = request.POST.get('email')
        # Код сброса пароля (как ранее)
        return render(request, 'accounts/reset_password.html', {'message': 'Check your email for reset instructions'})
    return render(request, 'accounts/reset_password.html')



def token_view(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user:
            refresh = RefreshToken.for_user(user)
            return render(request, 'accounts/tokens.html', {
                'access': str(refresh.access_token),
                'refresh': str(refresh)
            })
        return render(request, 'accounts/tokens.html', {'error': 'Invalid credentials'})
    return render(request, 'accounts/tokens.html')
