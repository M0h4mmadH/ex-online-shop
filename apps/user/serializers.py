from rest_framework import serializers
from .models import User


class UserRegisterInputSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    email = serializers.EmailField(required=False)
    phone_number = serializers.CharField(required=False)

    class Meta:
        model = User
        fields = ['phone_number', 'email', 'password']

    def validate(self, data):
        if not data.get('email') and not data.get('phone_number'):
            raise serializers.ValidationError("Either email or phone number must be provided.")
        return data


class UserRegisterOutputSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'phone_number', 'email']


class UserLoginInputSerializer(serializers.Serializer):
    login = serializers.CharField()
    password = serializers.CharField()


class UserLoginOutputSerializer(serializers.Serializer):
    access = serializers.CharField()
    refresh = serializers.CharField()


class OTPVerificationSerializer(serializers.Serializer):
    login = serializers.CharField()
    otp = serializers.CharField()
