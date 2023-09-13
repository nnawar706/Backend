from django.http import JsonResponse
from rest_framework.views import APIView
from rest_framework import status
from rest_framework import permissions
from rooms.models import ExamRoom
from .permissions import *
from .serializer import *

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
                'error': serializer.errors
            }, status = status.HTTP_422_UNPROCESSABLE_ENTITY)

        quiz = serializer.create(serializer.validated_data)

        return JsonResponse({'status': False}, status = status.HTTP_201_CREATED)


def validation_error(errors):
    error_field = next(iter(errors))
    return errors[error_field][0]