from django.http import JsonResponse
from rest_framework.views import APIView
from rest_framework import status
from rest_framework import permissions
from rooms.models import ExamRoom
from django.utils import timezone
from django.db.models import Count, Sum
from questions.models import SubQuestionMark
from .permissions import *
from .serializer import *
from .models import Quiz

class QuizCreateView (APIView):
    permission_classes = [permissions.IsAuthenticated, IsTeacher]

    def post (self, request, room_id):
        data = request.data

        try:
            room = ExamRoom.objects.get(pk=room_id)
        except ExamRoom.DoesNotExist:
            return JsonResponse({
            'status': False,
            'error': 'Room not found'}, status=status.HTTP_404_NOT_FOUND)

        serializer = QuizCreateSerializer(data = data, context={'request': request, 'room': room})

        if not serializer.is_valid():
            return JsonResponse({
                'status': False,
                'error': validation_error(serializer.errors)
            }, status = status.HTTP_422_UNPROCESSABLE_ENTITY)

        quiz = serializer.create(serializer.validated_data)

        return JsonResponse({'status': True}, status = status.HTTP_201_CREATED)

class QuizView (APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get (self, request, room_id):
        try:
            room = ExamRoom.objects.get(pk=room_id)
        except ExamRoom.DoesNotExist:
            return JsonResponse({
                'status': False,
                'error' : 'Room not found'
            }, status=status.HTTP_404_NOT_FOUND)
        
        if room.user != request.user:
            return JsonResponse({
                'status': False,
                'error' : 'You are not allowed to access this data.'
            }, status=status.HTTP_403_FORBIDDEN)
        
        data = room.quizzes.annotate(question_count=Count('questions')).order_by('-occurring_date')

        serializer = QuizzesSerializer(data, many=True)

        return JsonResponse({
            'status': True,
            'data': serializer.data
        }, status = status.HTTP_204_NO_CONTENT if len(serializer.data) == 0 else status.HTTP_200_OK)


class QuizUpdateView (APIView):
    permission_classes = [permissions.IsAuthenticated, IsTeacher]

    def put (self, request, pk):
        try:
            quiz = Quiz.objects.get(pk=pk)
        except ExamRoom.DoesNotExist:
            return JsonResponse({
                'status': False,
                'error': 'Quiz does not exist.'
            }, status = status.HTTP_404_NOT_FOUND)

        if quiz.room.user != request.user or quiz.occurring_date <= timezone.now().date():
            return JsonResponse({
                'status': False,
                'error': 'You are not allowed to perform this task.'
            }, status = status.HTTP_403_FORBIDDEN)

        data = request.data

        serializer = QuizUpdateSerializer(instance = quiz, data = data)

        if not serializer.is_valid():
            return JsonResponse({
                'status': False,
                'error': validation_error(serializer.errors)
            }, status = status.HTTP_422_UNPROCESSABLE_ENTITY)

        quiz = serializer.update(instance = quiz, data = serializer.validated_data)

        return JsonResponse({
            'status': True,
        }, status = status.HTTP_200_OK)


class QuizMarksView(APIView):
    permissions = [permissions.IsAuthenticated]

    def get (self, request, pk):
        try:
            quiz = Quiz.objects.get(pk=pk)
        except ExamRoom.DoesNotExist:
            return JsonResponse({
                'status': False,
                'error': 'Quiz does not exist.'
            }, status = status.HTTP_404_NOT_FOUND)

        if request.user.role == 2 and quiz.room.user != request.user:
            return JsonResponse({
                'status': False,
                'error': 'You are not authorized to perform this action.'
            }, status = status.HTTP_403_FORBIDDEN)

        mark_sheet = SubQuestionMark.objects.filter(
                         sub_question__question__quiz_id=quiz.id
                     ).values('student').annotate(
                         total_marks=Sum('mark')
                     ).order_by('student')
        print(mark_sheet)
        serializer = MarkSheetSerializer(mark_sheet, many=True)

        return JsonResponse({
            'status': True,
            'data': serializer.data
        }, status = status.HTTP_200_OK)

def validation_error(errors):
    error_field = next(iter(errors))
    return errors[error_field][0]