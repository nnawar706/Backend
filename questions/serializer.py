from rest_framework import serializers
from django.conf import settings
from .models import QuestionType, Question, SubQuestion, SubQuestionAnswer
from quizzes.models import Quiz
from django.utils import timezone


class AnswerSerializer (serializers.Serializer):
    answer = serializers.CharField()
    status = serializers.IntegerField()


class SubQuestionSerializer (serializers.Serializer):
    question    = serializers.CharField()
    sub_mark    = serializers.FloatField()
    answers     = AnswerSerializer(many=True)


class QuestionSerializer (serializers.Serializer):
    question_type_id = serializers.IntegerField()
    description      = serializers.CharField()
    total            = serializers.FloatField()
    sub_questions    = SubQuestionSerializer(many=True)


class QuestionCreateSerializer(serializers.Serializer):
    quiz_id     = serializers.IntegerField()
    questions   = QuestionSerializer(many=True)

    def __init__(self, *args, **kwargs):
        context = kwargs.pop('context', {})
        self.request = context.get('request')
        super().__init__(*args, **kwargs)

    def validate(self, data):
        quiz = Quiz.objects.filter('id', data['quiz_id']).first()

        if not quiz:
            raise serializers.ValidationError('Invalid quiz.')

        if quiz.occurring_date < timezone.now().date():
            raise serializers.ValidationError('Cannot add questions to a quiz that has passed.')

        if quiz.questions.count() > 0:
            raise serializers.ValidationError('Question has already been created for this quiz.')

        if quiz.room.user != request.user:
            raise serializers.ValidationError('Cannot add quiz questions .')

        for question in data['questions']:
            sub_mark_total = sum(sub_question['sub_mark'] for sub_question in question['sub_questions'])

            if sub_mark_total != question['total']:
                raise serializers.ValidationError('Total of sub question marks must be equal to total marks of a question.')

            for sub_question in question['sub_questions']:
                answers = sub_question['answers']

                if len(answers) < 2:
                    raise serializers.ValidationError('Each sub questions must have at least 2 choices for answers.')

                if not any(answer['status'] != 1 for answer in answers):
                    raise serializers.ValidationError('Each sub question must have at least 1 correct answer.')

        return data
