from rest_framework import serializers
from .models import User


class UserSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    email = serializers.EmailField(required=True,  max_length=255)
    full_name = serializers.CharField(
        required=False, allow_blank=True,  max_length=100)
    phone_number = serializers.IntegerField(read_only=True)
    address = serializers.CharField(allow_blank=True, allow_null=True)

    def update(self, instance, validated_data):
        if not instance.is_staff:
            instance.email = validated_data.get('email', instance.email)
            instance.full_name = validated_data.get('full_name', instance.full_name)
            instance.address = validated_data.get('address', instance.address)
            instance.save()
            return instance
        else:
            return instance