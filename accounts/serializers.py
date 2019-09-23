from rest_framework import serializers
from .models import User


class UserSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    email = serializers.EmailField(required=True,  max_length=255)
    full_name = serializers.CharField(
        required=False, allow_blank=True,  max_length=100)
    phone_number = serializers.IntegerField(read_only=True)
    address = serializers.CharField()