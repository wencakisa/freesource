from django.contrib.auth.models import User
from rest_framework import serializers


class UserReadSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('username',)


class UserLoginSerializer(serializers.ModelSerializer):
    username = serializers.CharField()
    password = serializers.CharField(
        write_only=True,
        required=True,
        style={'input_type': 'password'}
    )

    class Meta:
        model = User
        fields = ('username', 'password')
