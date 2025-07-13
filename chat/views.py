from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth import authenticate
from rest_framework.authtoken.models import Token
from .serializers import SignupSerializer, VerifySignupSerializer, LoginSerializer
from drf_yasg.utils import swagger_auto_schema

class SignupView(APIView):
    @swagger_auto_schema(request_body=SignupSerializer)
    def post(self, request):
        serializer = SignupSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "Foydalanuvchi yaratildi, emailga kod yuborildi"}, status=201)
        return Response(serializer.errors, status=400)

class VerifySignupView(APIView):
    @swagger_auto_schema(request_body=VerifySignupSerializer)
    def post(self, request):
        serializer = VerifySignupSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "Hisob tasdiqlandi"})
        return Response(serializer.errors, status=400)

class LoginView(APIView):
    @swagger_auto_schema(request_body=LoginSerializer)
    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            user = authenticate(
                email=serializer.validated_data['email'],
                password=serializer.validated_data['password']
            )
            if user and user.is_active:
                token, _ = Token.objects.get_or_create(user=user)
                return Response({"message": "Kirish muvaffaqiyatli", "token": token.key})
            return Response({"error": "Noto‘g‘ri email/parol yoki tasdiqlanmagan hisob"}, status=400)
        return Response(serializer.errors, status=400)
