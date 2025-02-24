from django.contrib.auth import login
from django.contrib.auth.models import User
from django.contrib.auth.tokens import default_token_generator
from django.forms import ValidationError
from django.shortcuts import get_object_or_404
from django.utils.http import urlsafe_base64_decode
from rest_framework import permissions
from rest_framework.authentication import authenticate
from rest_framework.exceptions import AuthenticationFailed
from rest_framework.response import Response
from rest_framework.views import APIView
from users.serializers import UserRegistrationSerializer
from users.tasks import send_verification_email
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView


class UserRegistrationView(APIView):
    def post(self, request):
        serializer = UserRegistrationSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            send_verification_email(user.username)
            return Response(
                {"msg": "account successfully created,please verify your email"}
            )
        return Response(serializer.errors, status=400)


class EmailVerify(APIView):
    def get(self, request, uidb64, token):
        user = self.get_user(uidb64)
        if user is None or not default_token_generator.check_token(user, token):
            return Response({"Couldn't verify"}, status=400)
        user.is_active = True
        user.save()
        login(request, user)
        return Response({"your email verified!"})

    @staticmethod
    def get_user(uidb64):
        try:
            uid = urlsafe_base64_decode(uidb64).decode()
            user = get_object_or_404(User, pk=uid)
        except (
            TypeError,
            ValueError,
            OverflowError,
            User.DoesNotExist,
            ValidationError,
        ):
            user = None
        return user
