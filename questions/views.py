from django.http import JsonResponse
from rest_framework.views import APIView
from rest_framework import status
from rest_framework import permissions
from quizzes.models import Quiz
from django.db.models import Sum
from .models import SubQuestion, SubQuestionMark
from .utils import render_to_pdf
from django.utils import timezone
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

        try:
            question = serializer.create(serializer.validated_data)
        except Exception as e:
            return JsonResponse({
                'status': False,
                'error': str(e)
            }, status = status.HTTP_500_INTERNAL_SERVER_ERROR)

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

        if request.user.role == 3 and (quiz.occurring_date > timezone.now().date() or (quiz.occurring_date == timezone.now().date() and timezone.now().time() < quiz.from_time)):
            return JsonResponse({
                'status': False,
                'error': 'You are not allowed to access this before ' + str(quiz.occurring_date.strftime('%d-%m-%Y')) + ' ' + str(quiz.from_time.strftime('%H:%M')) + '.'
            }, status=status.HTTP_403_FORBIDDEN)

        if request.user.role == 2 or (request.user.role == 3 and (quiz.occurring_date < timezone.now().date() or (quiz.occurring_date == timezone.now().date() and quiz.to_time < timezone.now().time()))):
            access_answer = True
        else:
            access_answer = False

        serializer = RetrieveQuestionModelSerializer(list(quiz.questions.all()), many=True, context={'send_answers': access_answer})

        return JsonResponse({
            'status':True,
            'data': serializer.data
        }, status=status.HTTP_200_OK)


class QuestionPdfView (APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get (self, request, quiz_id):
        try:
            quiz = Quiz.objects.get(pk=quiz_id)
        except Quiz.DoesNotExist:
            return JsonResponse({
                'status': False,
                'error': 'Quiz not found'
            }, status=status.HTTP_404_NOT_FOUND)

        if request.user.role == 2 and quiz.room.user != request.user:
            return JsonResponse({
                'status': False,
                'error': 'You are not allowed to access this data.'
            }, status=status.HTTP_403_FORBIDDEN)

        if request.user.role == 3 and (quiz.occurring_date > timezone.now().date() or (quiz.occurring_date == timezone.now().date() and timezone.now().time() < quiz.from_time)):
            return JsonResponse({
                'status': False,
                'error': 'You are not allowed to access this before ' + str(quiz.occurring_date.strftime('%d-%m-%Y')) + ' ' + str(quiz.from_time.strftime('%H:%M')) + '.'
            }, status=status.HTTP_403_FORBIDDEN)

        if request.user.role == 2 or (request.user.role == 3 and (quiz.occurring_date < timezone.now().date() or (quiz.occurring_date == timezone.now().date() and quiz.to_time < timezone.now().time()))):
            access_answer = True
        else:
            access_answer = False

        serializer = RetrieveQuestionModelSerializer(list(quiz.questions.all()), many=True, context={'send_answers': True})

        return render_to_pdf ('question.html', {'data': serializer.data})


class AnswerSubQuestionsView (APIView):
    permission_classes = [permissions.IsAuthenticated, IsStudent]

    def post (self, request, pk):
        try:
            sq = SubQuestion.objects.get(pk=pk)
        except SubQuestion.DoesNotExist:
            return JsonResponse({
                'status': False,
                'error': 'Question not found'
            }, status=status.HTTP_404_NOT_FOUND)

        if sq.question.quiz.occurring_date != timezone.now().date() or timezone.now().time() not in (sq.question.quiz.from_time, sq.question.quiz.to_time):
            return JsonResponse({
                'status': False,
                'error': 'You are not allowed to perform this action.'
            }, status=status.HTTP_403_FORBIDDEN)

        data = request.data
        serializer = AnswerSubQuestionsSerializer(data = data, context = {'request':request, 'sq': sq})

        if not serializer.is_valid():
            return JsonResponse({
                'status': False,
                'error': validation_error(serializer.errors)
            }, status = status.HTTP_422_UNPROCESSABLE_ENTITY)

        data = serializer.store_answer(serializer.validated_data)

        return JsonResponse({
            'status':True,
        }, status=status.HTTP_201_CREATED)


class QuizObtainedMarksView (APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get (self, request, quiz_id):
        try:
            quiz = Quiz.objects.get(pk=quiz_id)
        except Quiz.DoesNotExist:
            return JsonResponse({
                'status': False,
                'error': 'Quiz not found'
            }, status=status.HTTP_404_NOT_FOUND)

        if request.user.role == 2 and quiz.room.user != request.user:
            return JsonResponse({
                'status': False,
                'error': 'You are not allowed to access this data.'
            }, status=status.HTTP_403_FORBIDDEN)

        if request.user.role == 3 and not quiz.room.students.filter(id=request.user.id).exists():
            return JsonResponse({
                'status': False,
                'error': 'You are not allowed to access this data.'
            }, status=status.HTTP_403_FORBIDDEN)

        data = SubQuestionMark.objects.values('student__id','student__email').annotate(total_marks=Sum('mark'))

        return JsonResponse({
            'status': True,
            'data': list(data)
        }, status=status.HTTP_200_OK)


def validation_error(errors):
    error_field = next(iter(errors))
    return errors[error_field][0]