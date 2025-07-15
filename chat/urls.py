from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import SignupView, VerifyLoginView, UserListView, MaqolaViewSet, MaqolaFileDownloadView

router = DefaultRouter()
router.register(r'maqola', MaqolaViewSet, basename='maqola')

urlpatterns = [
    path('signup/', SignupView.as_view()),
    path('verify-login/', VerifyLoginView.as_view()),
    path('users/', UserListView.as_view()),
    path('maqolalar/<int:pk>/download/', MaqolaFileDownloadView.as_view(), name='maqola-download'),

    path('', include(router.urls)),  # bu yerda maxsulotlar uchun CRUD endpointlar avtomatik yaratiladi
]
