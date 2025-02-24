from django.contrib.auth.models import User
from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from users.views import UserRegistrationView, EmailVerify

urlpatterns = [
    path("registration/", UserRegistrationView.as_view()),
    path("login/", TokenObtainPairView.as_view(), name="login"),
    path("token/refresh/", TokenRefreshView.as_view()),
    path("verify-email/<uidb64>/<token>/", EmailVerify.as_view(), name="verify_email"),
]
