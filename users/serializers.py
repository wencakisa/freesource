from django.contrib.auth.models import User
from rest_framework import serializers
from rest_framework.validators import UniqueValidator
from rest_framework.authtoken.models import Token


class UserReadSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('username',)


class UserRegisterSerializer(serializers.ModelSerializer):
    username = serializers.CharField(
        required=True,
        min_length=3,
        max_length=30,
        validators=[
            UniqueValidator(
                queryset=User.objects.all(),
                message='User with this username already exists.'
            )
        ]
    )
    first_name = serializers.CharField(required=True, max_length=50)
    last_name = serializers.CharField(required=True, max_length=50)
    password = serializers.CharField(
        write_only=True,
        required=True,
        min_length=6,
        error_messages={
            'blank': 'Password cannot be empty.',
            'min_length': 'Password too short.',
        },
        style={'input_type': 'password'}
    )


    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'password')

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        Token.objects.create(user=user)

        return user


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
