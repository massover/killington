from django.contrib.auth import get_user_model
from rest_framework import serializers

from ..models import SES


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = get_user_model()
        fields = ('id', 'email',)


class SESSerializer(serializers.ModelSerializer):
    user = UserSerializer()

    class Meta:
        model = SES
        fields = ('id', 'email', 'user', )
