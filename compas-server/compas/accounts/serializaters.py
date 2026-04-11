from rest_framework import serializers
from django.contrib.auth import get_user_model

User = get_user_model()

class UserRegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, min_length=8, max_length=64)
    password2 = serializers.CharField(write_only=True, min_length=8, max_length=64)

    class Meta:
        model = User
        fields = ['username', 'email', 'name', 'lastname', 'password', 'password2']

    def validate(self, data):
        if data['password'] != data['password2']:
            raise serializers.ValidationError('Passwords must match.')

        return data

    def create(self, validated_data):
        validated_data.pop('password2')
        user = User.objects.create(**validated_data)
        return user

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name']
