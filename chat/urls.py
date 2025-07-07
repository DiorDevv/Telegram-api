from django.urls import path
from .views import RequestCodeView, VerifyCodeView

urlpatterns = [
    path('send-email/', RequestCodeView.as_view()),
    path('verify-code/', VerifyCodeView.as_view()),
]
