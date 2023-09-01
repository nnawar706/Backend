from rest_framework import serializers
from django.contrib.auth import get_user_model

User = get_user_model()

class UserSerializer (serializers.ModelSerializer):
    class Meta:
        model = User
        exclude = ('password')

    def validate(self, data):
        name = data['name']

        if len(name) < 5:
            raise serializers.ValidationError('Name field must be at least 5 characters long.')
        
        return data