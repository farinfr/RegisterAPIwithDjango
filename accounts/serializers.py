from rest_framework import serializers
from .models import User, OTP, LoginAttempt
from django.contrib.auth import get_user_model

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'password']

class OTPSerializer(serializers.ModelSerializer):
    class Meta:
        model = OTP
        fields = ['phone_number', 'code']

class PhoneSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['phone_number']


class LoginSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['phone_number', 'password']

