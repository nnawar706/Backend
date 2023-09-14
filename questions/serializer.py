from rest_framework import serializers
from django.conf import settings
from .models import QuestionType, Question, SubQuestion, SubQuestionAnswer


class QuestionCreatePayloadSerializer(serializers.Serializer):

