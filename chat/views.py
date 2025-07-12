from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.authtoken.models import Token
from django.contrib.auth import authenticate
from .serializers import (
    SignupSerializer, LoginSerializer,
    ResetPasswordRequestSerializer, VerifyResetCodeSerializer, ResetPasswordSerializer
)
from drf_yasg.utils import swagger_auto_schema

class SignupView(APIView):
    @swagger_auto_schema(request_body=SignupSerializer)
    def post(self, request):
        serializer = SignupSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "Parol emailga yuborildi"}, status=201)
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
            if user:
                token, _ = Token.objects.get_or_create(user=user)
                return Response({"message": "Muvaffaqiyatli login", "token": token.key})
            return Response({"error": "Email yoki parol noto‘g‘ri"}, status=400)
        return Response(serializer.errors, status=400)

class ResetPasswordRequestView(APIView):
    @swagger_auto_schema(request_body=ResetPasswordRequestSerializer)
    def post(self, request):
        serializer = ResetPasswordRequestSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "Kod emailga yuborildi"})
        return Response(serializer.errors, status=400)

class VerifyResetCodeView(APIView):
    @swagger_auto_schema(request_body=VerifyResetCodeSerializer)
    def post(self, request):
        serializer = VerifyResetCodeSerializer(data=request.data)
        if serializer.is_valid():
            return Response({"message": "Kod tasdiqlandi"})
        return Response(serializer.errors, status=400)

class ResetPasswordView(APIView):
    @swagger_auto_schema(request_body=ResetPasswordSerializer)
    def post(self, request):
        serializer = ResetPasswordSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "Parol yangilandi"})
        return Response(serializer.errors, status=400)

