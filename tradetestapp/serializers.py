import requests
from django.conf import settings
from rest_framework import serializers

from tradetestapp.models import Post, User, Like


class PostSerializer(serializers.ModelSerializer):

    class Meta:
        model = Post
        fields = ('id', 'author', 'content')
        read_only_fields = ('author',)


def email_validator(value):
    if settings.HUNTER_ENABLE:
        result = requests.get(
            "https://api.hunter.io/v2/email-verifier",
            params={'email': value, 'api_key': settings.HUNTER_IO_API_KEY}
        )
        data = result.json()
        if result.status_code != 200:
            errors = [e['details'] for e in data['errors']]
            raise serializers.ValidationError(errors)
    return value


class UserSerializer(serializers.ModelSerializer):
    email = serializers.CharField(validators=[email_validator])

    class Meta:
        model = User
        fields = ('username', 'password', 'email')
        extra_kwargs = {
            "password": {"write_only": True},
        }

    def create(self, validated_data):
        user = super(UserSerializer, self).create(validated_data)
        user.set_password(validated_data['password'])
        user.save()
        return user


class LikeSerializer(serializers.ModelSerializer):
    is_like = serializers.BooleanField(read_only=True)
    post = serializers.CharField(read_only=True)
    user = serializers.CharField(read_only=True)

    class Meta:
        model = Like
        fields = ('id', 'is_like', 'post', 'user')

    def create(self, validated_data):
        instance, _ = Like.objects.update_or_create(
            **validated_data, defaults={'is_like': True}
        )
        return instance


class UnlikeSerializer(serializers.ModelSerializer):
    is_like = serializers.BooleanField(read_only=True)
    post = serializers.CharField(read_only=True)
    user = serializers.CharField(read_only=True)

    class Meta:
        model = Like
        fields = ('id', 'is_like', 'post', 'user')

    def create(self, validated_data):
        instance, _ = Like.objects.update_or_create(
            **validated_data, defaults={'is_like': False}
        )
        return instance
