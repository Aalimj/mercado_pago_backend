from rest_framework import serializers
from django.contrib.auth import get_user_model,authenticate
from django.contrib.auth.password_validation import validate_password
from django.db import transaction
from wallets.models import Wallet
from rest_framework_simplejwt.tokens import RefreshToken

User = get_user_model()


class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, validators=[validate_password])
    password2 = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = (
            "name",
            "email",
            "cpf",
            "phone",
            "password",
            "password2",
        )

    def validate(self, attrs):
        if attrs["password"] != attrs["password2"]:
            raise serializers.ValidationError({"password": "Passwords must match"})
        return attrs

    def validate_cpf(self, value):
        if User.objects.filter(cpf=value).exists():
            raise serializers.ValidationError("CPF already registered")
        return value

    @transaction.atomic
    def create(self, validated_data):
        password = validated_data.pop("password")
        validated_data.pop("password2")

        user = User(**validated_data)
        user.set_password(password)
        user.save()

        

        return user

class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)

    def validate(self, attrs):
        user = authenticate(
            email=attrs["email"],
            password=attrs["password"]

        )

        if not user:
            raise serializers.ValidationError("Invalid email or password")
        
        if not user.is_active:
            raise serializers.ValidationError("User is disabled")
        
        refresh = RefreshToken.for_user(user)

        attrs["user"] = user
        return attrs
        
      

