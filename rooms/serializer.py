from rest_framework import serializers
from .models import ExamRoom

class ExamRoomCreateSerializer (serializers.ModelSerializer):
    class Meta:
        model = ExamRoom
        fields = ['user', 'title', 'detail', 'secret']


class ExamRoomSerializer (serializers.ModelSerializer):

    class Meta:
        model = ExamRoom
        exclude = ['secret']