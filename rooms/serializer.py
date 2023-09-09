from rest_framework import serializers
from rest_framework.validators import UniqueTogetherValidator
from .models import ExamRoom
import hashlib
import uuid

class ExamRoomCreateSerializer (serializers.ModelSerializer):

    class Meta:
        model = ExamRoom
        fields = ['title', 'detail', 'secret']

    def validate(self, data):
        if len(data['title']) < 5:
            raise serializers.ValidationError('Title field must be at least 5 characters long.')

        return data

    def create(self, data):
        user = request.user

        room = ExamRoom(
            user    = user,
            title   = data['title'],
            detail  = data['detail'],
            secret  = generate_token(data['secret'])
        )

        return room


class ExamRoomSerializer (serializers.ModelSerializer):

    class Meta:
        model = ExamRoom
        exclude = ['secret']


def generate_token(code):
    salt = uuid.uuid4().hex
    secret = hashlib.sha256(salt.encode() + code.encode()).hexdigest() + ':' + salt
    return secret