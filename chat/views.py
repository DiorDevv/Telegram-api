from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.authtoken.models import Token
from .serializers import RequestCodeSerializer, VerifyCodeSerializer
from drf_yasg.utils import swagger_auto_schema
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.authtoken.models import Token
from drf_yasg.utils import swagger_auto_schema
from .serializers import RequestCodeSerializer, VerifyCodeSerializer


class RequestCodeView(APIView):
    @swagger_auto_schema(request_body=RequestCodeSerializer)
    def post(self, request):
        serializer = RequestCodeSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "Tasdiqlash kodi yuborildi"})
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class VerifyCodeView(APIView):
    @swagger_auto_schema(request_body=VerifyCodeSerializer)
    def post(self, request):
        serializer = VerifyCodeSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            token, _ = Token.objects.get_or_create(user=user)
            return Response({"message": "Login muvaffaqiyatli", "token": token.key})
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
