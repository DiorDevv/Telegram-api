# chat/views.py

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from .models import User, EmailCode
from .serializers import SignupSerializer, LoginSerializer
from drf_yasg.utils import swagger_auto_schema

class SignupView(APIView):
    @swagger_auto_schema(request_body=SignupSerializer)
    def post(self, request):
        serializer = SignupSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "Foydalanuvchi yaratildi, emailga kod yuborildi"}, status=201)
        return Response(serializer.errors, status=400)

class LoginView(APIView):
    @swagger_auto_schema(request_body=LoginSerializer)
    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            user = User.objects.get(email=serializer.validated_data['email'])
            user.is_active = True
            user.save()

            EmailCode.objects.filter(email=user.email).delete()

            token, _ = Token.objects.get_or_create(user=user)
            return Response({
                "message": "Kirish muvaffaqiyatli",
                "token": token.key
            })
        return Response(serializer.errors, status=400)
