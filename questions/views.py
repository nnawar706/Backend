from django.http import JsonResponse
from rest_framework.views import APIView
from rest_framework import status
from rest_framework import permissions
from quizzes.models import Quiz
from .serializer import *
from .permissions import *


class QuestionCreateView (APIView):
    permission_classes = [permissions.IsAuthenticated, IsTeacher]

    def post (self, request):
        data = request.data

        serializer = QuestionCreateSerializer (data = data, context = {'request': request})

        if not serializer.is_valid():
            return JsonResponse({
                'status': False,
                'error': serializer.errors
            }, status = status.HTTP_422_UNPROCESSABLE_ENTITY)

#         try:
#             question = serializer.create(serializer.validated_data)
#         except Exception as e:
#             return JsonResponse({
#                 'status': False,
#                 'error': str(e)
#             }, status = status.HTTP_500_INTERNAL_SERVER_ERROR)

        return JsonResponse({'status': True}, status = status.HTTP_201_CREATED)


class QuestionView (APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get (self, request, quiz_id):
        try:
            quiz = Quiz.objects.get(pk=quiz_id)
        except Quiz.DoesNotExist:
            return JsonResponse({
                'status': False,
                'error': 'Quiz not found'
            }, status=status.HTTP_404_NOT_FOUND)

        if quiz.room.user != request.user:
            return JsonResponse({
                'status': False,
                'error': 'You are not allowed to access this data.'
            }, status=status.HTTP_403_FORBIDDEN)

        serializer = RetrieveQuestionModelSerializer(list(quiz.questions.all()), many=True)

        return JsonResponse({
            'status':True,
            'data': serializer.data
        }, status=status.HTTP_200_OK)