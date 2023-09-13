from django.http import JsonResponse
from rest_framework.views import APIView
from rest_framework import status
from rest_framework import permissions
from .permissions import *
from .serializer import *

class QuizCreateView (APIView):
    permission_classes = [permissions.IsAuthenticated, IsTeacher]

    def post (self, request):
        data = request.data

        serializer = QuizCreateSerializer(data = data, context={'request': request})

        if not serializer.is_valid():
            return JsonResponse({
                'status': False,
                'error': validation_error(serializer.errors)
            }, status = status.HTTP_422_UNPROCESSABLE_ENTITY)

        quiz = serializer.create(serializer.validated_data)

        return JsonResponse({'status': False}, status = status.HTTP_201_CREATED)


def validation_error(errors):
    error_field = next(iter(errors))
    return errors[error_field][0]