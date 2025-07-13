# chat/urls.py

from django.urls import path
from .views import SignupView, LoginView, ListUsersView

urlpatterns = [
    path('signup/', SignupView.as_view()),
    path('login/', LoginView.as_view()),
    path('users/', ListUsersView.as_view()),
]
