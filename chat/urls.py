
# urls.py
from django.urls import path
from .views import (
    SignupView, LoginView,
    ResetPasswordRequestView, VerifyResetCodeView, ResetPasswordView
)

urlpatterns = [
    path('signup/', SignupView.as_view()),
    path('login/', LoginView.as_view()),
    path('reset-password-request/', ResetPasswordRequestView.as_view()),
    path('verify-reset-code/', VerifyResetCodeView.as_view()),
    path('reset-password/', ResetPasswordView.as_view()),
]