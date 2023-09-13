from rest_framework import serializers
from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password
from django.core import exceptions

User = get_user_model()

class UserCreateSerializer (serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ['id', 'name', 'email', 'password', 'role']

    def validate(self, data):
        name = data['name']

        if len(name) < 5:
            raise serializers.ValidationError('Name field must be at least 5 characters long.')

        try:
            validate_password(data['password'])
        except exceptions.ValidationError as e:
            raise serializers.ValidationError(serializers.as_serializer_error(e)['non_field_errors'])

        return data
    
    def create(self, data):
        user = User.objects.create_user(
            name = data['name'],
            email = data['email'],
            password = data['password'],
            role = data['role']
        )

        return user


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        exclude = ['password']


class AccessUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id','email','name']