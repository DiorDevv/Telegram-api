from django.urls import path
from .views import SignupView, VerifyLoginView

urlpatterns = [
    path('signup/', SignupView.as_view()),
    path('verify-login/', VerifyLoginView.as_view()),
]
