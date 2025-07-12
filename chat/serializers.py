# serializers.py
from rest_framework import serializers
from .models import User, ResetCode
import random
import string
from django.core.mail import send_mail

class SignupSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            'first_name', 'last_name', 'gender', 'institute', 'specialty', 'country',
            'city', 'address', 'postal_code', 'phone', 'email'
        ]

    def create(self, validated_data):
        password = ''.join(random.choices(string.ascii_letters + string.digits, k=8))
        user = User.objects.create_user(password=password, **validated_data)

        send_mail(
            subject="Sizning parolingiz",
            message=f"Hurmatli {user.first_name}, sizning parolingiz: {password}",
            from_email=None,
            recipient_list=[user.email],
            fail_silently=False
        )
        return user

class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)

class ResetPasswordRequestSerializer(serializers.Serializer):
    email = serializers.EmailField()

    def validate_email(self, value):
        if not User.objects.filter(email=value).exists():
            raise serializers.ValidationError("Bunday email ro'yxatdan o'tmagan.")
        return value

    def create(self, validated_data):
        email = validated_data['email']
        ResetCode.objects.filter(email=email).delete()
        code = str(random.randint(100000, 999999))
        ResetCode.objects.create(email=email, code=code)

        send_mail(
            "Parolni tiklash kodingiz",
            f"Sizning tasdiqlash kodingiz: {code}",
            from_email=None,
            recipient_list=[email],
            fail_silently=False
        )
        return {"message": "Emailga kod yuborildi"}

class VerifyResetCodeSerializer(serializers.Serializer):
    email = serializers.EmailField()
    code = serializers.CharField(max_length=6)

    def validate(self, data):
        try:
            obj = ResetCode.objects.get(email=data['email'], code=data['code'])
        except ResetCode.DoesNotExist:
            raise serializers.ValidationError("Kod noto‘g‘ri")
        if obj.is_expired():
            raise serializers.ValidationError("Kod eskirgan")
        return data

class ResetPasswordSerializer(serializers.Serializer):
    email = serializers.EmailField()
    code = serializers.CharField(max_length=6)
    new_password = serializers.CharField(write_only=True)

    def validate(self, data):
        try:
            obj = ResetCode.objects.get(email=data['email'], code=data['code'])
        except ResetCode.DoesNotExist:
            raise serializers.ValidationError("Kod noto‘g‘ri")
        if obj.is_expired():
            raise serializers.ValidationError("Kod eskirgan")
        data['user'] = User.objects.get(email=data['email'])
        obj.delete()
        return data

    def create(self, validated_data):
        user = validated_data['user']
        user.set_password(validated_data['new_password'])
        user.save()
        return {"message": "Parol yangilandi"}
