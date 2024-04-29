from rest_framework import serializers

from .models import User


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['phone_number']
        read_only_fields = ['invite_code', 'activated_invite_code']


class UserProfileSerializer(serializers.ModelSerializer):
    invited_users = serializers.StringRelatedField(read_only=True, many=True)

    class Meta:
        model = User
        fields = ['activated_invite_code', 'invited_users']
        read_only_fields = ['phone_number', 'invited_users']