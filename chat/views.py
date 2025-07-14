from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.viewsets import ModelViewSet
from rest_framework_simplejwt.tokens import RefreshToken
from .serializers import SignupSerializer, VerifyLoginSerializer, UserSerializer, MaqolaSerializer
from .models import EmailCode, User, Maqola
from drf_yasg.utils import swagger_auto_schema
from rest_framework.parsers import MultiPartParser, FormParser


class SignupView(APIView):
    @swagger_auto_schema(request_body=SignupSerializer)
    def post(self, request):
        serializer = SignupSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "Kod emailga yuborildi"}, status=201)
        return Response(serializer.errors, status=400)


class VerifyLoginView(APIView):
    @swagger_auto_schema(request_body=VerifyLoginSerializer)
    def post(self, request):
        serializer = VerifyLoginSerializer(data=request.data)
        if serializer.is_valid():
            email = serializer.validated_data['email']
            code = serializer.validated_data['code']

            try:
                email_code = EmailCode.objects.get(email=email, code=code)
                if email_code.is_expired():
                    return Response({"error": "Kod eskirgan"}, status=400)
            except EmailCode.DoesNotExist:
                return Response({"error": "Noto‘g‘ri kod"}, status=400)

            user = User.objects.get(email=email)
            user.is_active = True
            user.save()
            EmailCode.objects.filter(email=email).delete()

            refresh = RefreshToken.for_user(user)
            return Response({
                "message": "Muvaffaqiyatli login",
                "user": UserSerializer(user).data,
                "access": str(refresh.access_token),
                "refresh": str(refresh)
            })
        return Response(serializer.errors, status=400)


class UserListView(APIView):
    def get(self, request):
        users = User.objects.all()
        serializer = UserSerializer(users, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class MaqolaViewSet(ModelViewSet):
    queryset = Maqola.objects.all()
    serializer_class = MaqolaSerializer
    parser_classes = [MultiPartParser, FormParser]

    def perform_create(self, serializer):
        serializer.save()

