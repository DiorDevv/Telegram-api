from rest_framework import serializers
from .models import User, EmailCode
import random
from django.core.mail import send_mail

class RequestCodeSerializer(serializers.Serializer):
    email = serializers.EmailField()

    def create(self, validated_data):
        email = validated_data['email']

        # eski kodlarni tozalash
        EmailCode.objects.filter(email=email).delete()

        # yangi kod
        code = str(random.randint(100000, 999999))
        EmailCode.objects.create(email=email, code=code)

        # real email yuborish
        send_mail(
            subject="Sizning tasdiqlash kodingiz",
            message=f"Tasdiqlash kodingiz: {code}",
            from_email=None,  # DEFAULT_FROM_EMAIL ishlaydi
            recipient_list=[email],
            fail_silently=False
        )

        return {"message": "Tasdiqlash kodi yuborildi"}

class VerifyCodeSerializer(serializers.Serializer):
    email = serializers.EmailField()
    code = serializers.CharField(max_length=6)

    def validate(self, data):
        email = data['email']
        code = data['code']
        try:
            obj = EmailCode.objects.get(email=email, code=code)
        except EmailCode.DoesNotExist:
            raise serializers.ValidationError("Noto'g'ri kod")

        if obj.is_expired():
            raise serializers.ValidationError("Kod eskirgan")

        data['obj'] = obj
        return data

    def create(self, validated_data):
        obj = validated_data['obj']
        user, created = User.objects.get_or_create(email=obj.email)
        obj.delete()
        return user
