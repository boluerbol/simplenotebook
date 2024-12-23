from rest_framework.views import APIView
from django.views import View 
from rest_framework.response import Response
from rest_framework import status
from .serializers import RegisterSerializer
from rest_framework_simplejwt.tokens import RefreshToken
# from django.core.mail import send_mail, BadHeaderError
# from django.contrib.auth.tokens import PasswordResetTokenGenerator
# from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
# from django.conf import settings
from django.contrib.auth import authenticate, get_user_model
from rest_framework.permissions import IsAuthenticated
from .serializers import UserSerializer 
from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_decode
from django.contrib.auth import get_user_model
from django.shortcuts import render, redirect
from django.contrib.auth.forms import SetPasswordForm
from django.http import Http404
from rest_framework import status
from django.core.mail import send_mail, BadHeaderError
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.utils.http import urlsafe_base64_encode
from django.conf import settings


User = get_user_model()


class CurrentUserAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user  # The currently authenticated user
        serializer = UserSerializer(user)  # Use the new serializer
        return Response(serializer.data)

class RegisterAPIView(APIView):
    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            refresh = RefreshToken.for_user(user)
            return Response({
                "message": "User registered successfully!",
                "access": str(refresh.access_token),
                "refresh": str(refresh)
            }, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class LoginAPIView(APIView):
    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')
        user = authenticate(request, username=username, password=password)
        if user:
            refresh = RefreshToken.for_user(user)
            return Response({
                "message": "Login successful!",
                "access": str(refresh.access_token),
                "refresh": str(refresh)
            }, status=status.HTTP_200_OK)
        return Response({"error": "Invalid credentials"}, status=status.HTTP_401_UNAUTHORIZED)

class LogoutAPIView(APIView):
    def post(self, request):
        return Response({"message": "Logout successful!"}, status=status.HTTP_200_OK)


class ResetPasswordView(View):
    def get(self, request, uidb64, token):
        try:
            uid = urlsafe_base64_decode(uidb64).decode()
            user = get_user_model().objects.get(pk=uid)
        except (TypeError, ValueError, OverflowError, get_user_model().DoesNotExist):
            raise Http404("User not found")

        if default_token_generator.check_token(user, token):
            form = SetPasswordForm(user=user)
            return render(request, 'reset_password.html', {'form': form})
        else:
            return redirect('accounts:password_reset')  # Or an error page if the token is invalid
        
class ResetPasswordAPIView(APIView):
    def post(self, request):
        email = request.data.get('email')
        user = get_user_model().objects.filter(email=email).first()
        if not user:
            return Response({"error": "User with this email does not exist"}, status=status.HTTP_404_NOT_FOUND)

        reset_token = PasswordResetTokenGenerator().make_token(user)
        uid = urlsafe_base64_encode(force_bytes(str(user.pk)))


        reset_link = f"{settings.FRONTEND_URL}/reset-password/{uid}/{reset_token}/"
        print(reset_link)
        try:
            send_mail(
                subject="Password Reset",
                message=f"Click the link to reset your password: {reset_link}",
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[email],
            )
        except BadHeaderError:
            return Response({"error": "Invalid email header"}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        return Response({"message": "Check your email for reset instructions"}, status=status.HTTP_200_OK)
    

class ResetPasswordConfirmAPIView(APIView):
    def post(self, request, uidb64, token):
        try:
            # Decode the uid
            uid = urlsafe_base64_decode(uidb64).decode()
            user = User.objects.get(pk=uid)

            print("uid ========>",uid,"user========>",user,"token=============>")

            # Check the validity of the token
            if not PasswordResetTokenGenerator().check_token(user, token):
                return Response({"error": "Invalid or expired token"}, status=status.HTTP_403_FORBIDDEN)

            # Get the new password
            new_password = request.data.get("new_password")
            if not new_password:
                return Response({"error": "New password is required"}, status=status.HTTP_400_BAD_REQUEST)

            # Set the new password
            user.set_password(new_password)
            user.save()

            return Response({"message": "Password reset successful"}, status=status.HTTP_200_OK)

        except User.DoesNotExist:
            return Response({"error": "Invalid user"}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            # Log the error for further inspection (optional, for debugging purposes)
            # logger.error(f"Password reset failed: {str(e)}")
            return Response({"error": f"An error occurred: {str(e)}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class CurrentUserAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user  # The currently authenticated user
        serializer = UserSerializer(user)
        return Response(serializer.data)