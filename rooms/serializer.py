from rest_framework import serializers
from rest_framework.validators import UniqueTogetherValidator
from .models import ExamRoom
import secrets
import string

class ExamRoomCreateSerializer (serializers.ModelSerializer):

    class Meta:
        model = ExamRoom
        fields = ['title', 'detail']

    def __init__(self, *args, **kwargs):
        context = kwargs.pop('context', {})
        self.request = context.get('request')
        super().__init__(*args, **kwargs)

    def validate (self, data):
        existing_room = ExamRoom.objects.filter(user=self.request.user, title=data['title']).first()

        if existing_room:
            raise serializers.ValidationError('A room with the same title already exists.')

        if len(data['title']) < 5:
            raise serializers.ValidationError('Title field must be at least 5 characters long.')

        return data

    def create (self, data):
        room = ExamRoom(
            user    = self.request.user,
            title   = data['title'],
            detail  = data['detail'],
            secret  = generate_code(8)
        )

        room.save()

        return room


class ExamRoomSerializer (serializers.ModelSerializer):

    class Meta:
        model = ExamRoom
        exclude = ['user','secret']


class ExamRoomUpdateSerializer (serializers.ModelSerializer):

    class Meta:
        model = ExamRoom
        exclude = ['user','secret','created_at']

    def validate (self, data):
        instance = self.instance
        if 'title' in data and len(data['title']) < 5:
            raise serializers.ValidationError('Title field must be at least 5 characters long.')

        if 'title' in data and data['title'] != instance.title:
            existing_room = ExamRoom.objects.filter(user=instance.user, title=data['title']).first()
            if existing_room:
                raise serializers.ValidationError('A room with the same title already exists.')

        return data

    def update (self, instance, data):
        instance.title = data.get('title', instance.title)
        instance.detail = data.get('detail', instance.detail)
        instance.save()
        return instance


def generate_code (length=8):
    characters = string.digits
    random_string = ''.join(secrets.choice(characters) for _ in range(length))

    return random_string