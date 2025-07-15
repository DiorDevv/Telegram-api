from django.http import FileResponse, Http404
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.viewsets import ModelViewSet
from rest_framework_simplejwt.tokens import RefreshToken
from .serializers import SignupSerializer, VerifyLoginSerializer, UserSerializer, MaqolaSerializer, UserlistSerializer
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
                # EmailCode dan tekshir
                email_code = EmailCode.objects.get(email=email, code=code)

            except EmailCode.DoesNotExist:
                return Response({"error": "Kod noto‘g‘ri"}, status=400)

            try:
                user = User.objects.get(email=email)
            except User.DoesNotExist:
                return Response({"error": "Foydalanuvchi topilmadi"}, status=404)

            # Kodni parol sifatida tekshir
            if not user.check_password(code):
                return Response({"error": "Kod noto‘g‘ri (parol sifatida)"}, status=400)

            # Aktivlashtirish
            user.is_active = True
            user.save()

            # EmailCode'ni o‘chirmaymiz — keyinchalik ham ishlaydi

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
        users = User.objects.filter(is_staff=False, is_superuser=False)
        serializer = UserlistSerializer(users, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class MaqolaViewSet(ModelViewSet):
    queryset = Maqola.objects.all()
    serializer_class = MaqolaSerializer
    parser_classes = [MultiPartParser, FormParser]
    permission_classes = [AllowAny]

    def perform_create(self, serializer):
        serializer.save()

class MaqolaFileDownloadView(APIView):
    def get(self, request, pk):
        try:
            maqola = Maqola.objects.get(pk=pk)
            if maqola.file:
                response = FileResponse(maqola.file.open(), as_attachment=True)
                return response
            else:
                return Response({"detail": "Maqolada fayl yo‘q"}, status=status.HTTP_404_NOT_FOUND)
        except Maqola.DoesNotExist:
            raise Http404("Maqola topilmadi")