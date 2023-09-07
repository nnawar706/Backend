from rest_framework import serializers
from rest_framework.validators import UniqueTogetherValidator
from .models import ExamRoom

class ExamRoomCreateSerializer (serializers.ModelSerializer):
    class Meta:
        model = ExamRoom
        fields = ['user', 'title', 'detail', 'secret']

    def validate(self, data):
        if len(data['title']) < 5:
            raise serializers.ValidationError('Title field must be at least 5 characters long.')

        return data

    def create(self, data):
        room = ExamRoom(
            user =
            title = data['title'],
            detail = data['detail'],
            secret = data['secret']
        )

        return room


class ExamRoomSerializer (serializers.ModelSerializer):

    class Meta:
        model = ExamRoom
        exclude = ['secret']
