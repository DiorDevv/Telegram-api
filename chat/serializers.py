from rest_framework import serializers
from .models import User, EmailCode, Maqola, Category
from django.core.mail import send_mail
import random


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        exclude = ('password', 'groups', 'user_permissions')


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
            "Tasdiqlash kodingiz",
            f"Sizning tasdiqlash kodingiz: {code}",
            from_email=None,
            recipient_list=[user.email],
            fail_silently=False
        )
        return user


class VerifyLoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    code = serializers.CharField(max_length=6)


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'


class MaqolaSerializer(serializers.ModelSerializer):
    author = UserSerializer(read_only=True)
    author_id = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.all(),
        source='author',
        write_only=True,
        required=False
    )
    category = CategorySerializer(read_only=True)
    category_id = serializers.PrimaryKeyRelatedField(
        queryset=Category.objects.all(),
        source='category',
        write_only=True,
        required=False
    )

    class Meta:
        model = Maqola
        fields = '__all__'
