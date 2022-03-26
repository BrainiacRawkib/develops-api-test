from apiutils.utils import logger
from django.contrib.auth import authenticate
from rest_framework import serializers
from .models import User
from .utils import create_user, update_user, generate_token_for_user


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = [
            'code', 'username', 'email', 'password'
        ]
        read_only_fields = ['code']
        extra_kwargs = {
            'password': {'write_only': True}
        }

    def create(self, validated_data):
        try:
            return create_user(**validated_data), ""

        except Exception as err:
            logger.error('UserSerializer.create@Error')
            logger.error(err)
            return None, str(err)

    def update(self, instance, validated_data):
        try:
            return update_user(instance, validated_data), ""

        except Exception as err:
            logger.error('UserSerializer.update@Error')
            logger.error(err)
            return None, str(err)


class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField()
    token = serializers.CharField()

    def validate(self, attrs):
        username = attrs.get('username')
        password = attrs.get('password')

        user = authenticate(username=username, password=password)
        if user and user.is_active:
            return generate_token_for_user(user)
        return serializers.ValidationError('Invalid Login Credentials')