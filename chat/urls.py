# urls.py
from django.urls import path
from .views import SignupView, VerifySignupView, LoginView

urlpatterns = [
    path('signup/', SignupView.as_view()),
    path('verify-signup/', VerifySignupView.as_view()),
    path('login/', LoginView.as_view()),
]