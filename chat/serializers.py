# chat/serializers.py

from rest_framework import serializers
from .models import User, EmailCode
from django.core.mail import send_mail
import random

class SignupSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        exclude = ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions', 'last_login', 'password')

    def create(self, validated_data):
        code = str(random.randint(100000, 999999))
        user = User.objects.create_user(password=code, **validated_data)
        user.is_active = False
        user.save()

        EmailCode.objects.filter(email=user.email).delete()
        EmailCode.objects.create(email=user.email, code=code)

        send_mail(
            subject="Tasdiqlash kodingiz",
            message=f"Sizning kirish kodingiz: {code}",
            from_email=None,
            recipient_list=[user.email],
            fail_silently=False,
        )
        return user

class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    code = serializers.CharField(max_length=6)

    def validate(self, data):
        try:
            obj = EmailCode.objects.get(email=data['email'], code=data['code'])
        except EmailCode.DoesNotExist:
            raise serializers.ValidationError("Kod noto‘g‘ri")

        if obj.is_expired():
            raise serializers.ValidationError("Kod eskirgan")

        return data
